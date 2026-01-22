package com.mobileagentlivelink.data

import com.google.gson.Gson
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import okhttp3.*
import java.util.UUID
import java.util.concurrent.TimeUnit

/**
 * WebSocket 中转服务客户端
 */
class RelayClient(
    private val serverUrl: String,
    private val deviceId: String = UUID.randomUUID().toString().take(8)
) {
    private val client = OkHttpClient.Builder()
        .pingInterval(30, TimeUnit.SECONDS)
        .build()
    
    private var webSocket: WebSocket? = null
    private val gson = Gson()
    
    private val _connectionState = MutableStateFlow(ConnectionState.DISCONNECTED)
    val connectionState: StateFlow<ConnectionState> = _connectionState
    
    private val _pairedPcId = MutableStateFlow<String?>(null)
    val pairedPcId: StateFlow<String?> = _pairedPcId
    
    private val _onlinePcs = MutableStateFlow<List<String>>(emptyList())
    val onlinePcs: StateFlow<List<String>> = _onlinePcs
    
    val messageChannel = Channel<ServerMessage>(Channel.BUFFERED)
    
    fun connect() {
        if (_connectionState.value == ConnectionState.CONNECTING) return
        
        _connectionState.value = ConnectionState.CONNECTING
        
        val request = Request.Builder()
            .url(serverUrl)
            .build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                _connectionState.value = ConnectionState.CONNECTED
                // 注册设备
                send(mapOf(
                    "type" to "register",
                    "device_id" to deviceId,
                    "device_type" to "mobile"
                ))
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                handleMessage(text)
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                _connectionState.value = ConnectionState.DISCONNECTED
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                _connectionState.value = ConnectionState.DISCONNECTED
            }
        })
    }
    
    fun disconnect() {
        webSocket?.close(1000, "User disconnect")
        webSocket = null
        _connectionState.value = ConnectionState.DISCONNECTED
    }
    
    private fun send(data: Map<String, Any>) {
        webSocket?.send(gson.toJson(data))
    }
    
    private fun handleMessage(text: String) {
        try {
            val data = gson.fromJson(text, Map::class.java) as Map<String, Any>
            val type = data["type"] as? String ?: return
            
            when (type) {
                "registered" -> {
                    // 注册成功，获取 PC 列表
                    send(mapOf("type" to "list_pcs"))
                }
                "pc_list" -> {
                    val pcs = (data["pcs"] as? List<*>)?.mapNotNull { it as? String } ?: emptyList()
                    _onlinePcs.value = pcs
                }
                "pair_result" -> {
                    val success = data["success"] as? Boolean ?: false
                    if (success) {
                        _pairedPcId.value = data["pc_id"] as? String
                    }
                }
                "ack" -> {
                    val success = data["success"] as? Boolean ?: false
                    messageChannel.trySend(ServerMessage.Ack(success))
                }
                "status" -> {
                    val running = data["running"] as? Boolean ?: false
                    messageChannel.trySend(ServerMessage.Status(running))
                }
                "error" -> {
                    val msg = data["message"] as? String ?: "未知错误"
                    messageChannel.trySend(ServerMessage.Error(msg))
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    /** 获取在线 PC 列表 */
    fun refreshPcList() {
        send(mapOf("type" to "list_pcs"))
    }
    
    /** 配对 PC */
    fun pairWithPc(pcId: String) {
        send(mapOf(
            "type" to "pair",
            "pc_id" to pcId
        ))
    }
    
    /** 发送消息到 Cursor */
    fun sendToCursor(content: String) {
        send(mapOf(
            "type" to "send_to_cursor",
            "content" to content,
            "message_id" to UUID.randomUUID().toString()
        ))
    }
    
    /** 获取 PC 状态 */
    fun requestStatus() {
        send(mapOf("type" to "get_status"))
    }
}

enum class ConnectionState {
    DISCONNECTED, CONNECTING, CONNECTED
}

sealed class ServerMessage {
    data class Ack(val success: Boolean) : ServerMessage()
    data class Status(val cursorRunning: Boolean) : ServerMessage()
    data class Error(val message: String) : ServerMessage()
}
