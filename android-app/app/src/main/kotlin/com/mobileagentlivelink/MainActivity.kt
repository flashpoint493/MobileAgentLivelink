package com.mobileagentlivelink

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.mobileagentlivelink.data.RelayClient
import com.mobileagentlivelink.ui.MainScreen
import com.mobileagentlivelink.ui.theme.MobileAgentLivelinkTheme

class MainActivity : ComponentActivity() {
    
    // TODO: 从配置读取服务器地址
    private val relayClient = RelayClient(
        serverUrl = "ws://10.0.2.2:8765/ws", // 模拟器访问本机
        deviceId = "android-${System.currentTimeMillis() % 10000}"
    )
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            MobileAgentLivelinkTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen(relayClient)
                }
            }
        }
    }
    
    override fun onStart() {
        super.onStart()
        relayClient.connect()
    }
    
    override fun onStop() {
        super.onStop()
        relayClient.disconnect()
    }
}
