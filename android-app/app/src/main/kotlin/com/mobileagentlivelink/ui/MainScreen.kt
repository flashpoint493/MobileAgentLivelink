package com.mobileagentlivelink.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Computer
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mobileagentlivelink.data.ConnectionState
import com.mobileagentlivelink.data.RelayClient

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(relayClient: RelayClient) {
    val connectionState by relayClient.connectionState.collectAsState()
    val onlinePcs by relayClient.onlinePcs.collectAsState()
    val pairedPcId by relayClient.pairedPcId.collectAsState()
    
    var messageText by remember { mutableStateOf("") }
    var showPcDialog by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("MobileAgent Livelink") },
                actions = {
                    // 连接状态指示
                    val statusColor = when (connectionState) {
                        ConnectionState.CONNECTED -> MaterialTheme.colorScheme.primary
                        ConnectionState.CONNECTING -> MaterialTheme.colorScheme.tertiary
                        ConnectionState.DISCONNECTED -> MaterialTheme.colorScheme.error
                    }
                    Badge(containerColor = statusColor) {
                        Text(
                            when (connectionState) {
                                ConnectionState.CONNECTED -> "已连接"
                                ConnectionState.CONNECTING -> "连接中"
                                ConnectionState.DISCONNECTED -> "未连接"
                            },
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            // PC 连接状态卡片
            Card(
                modifier = Modifier.fillMaxWidth(),
                onClick = { 
                    relayClient.refreshPcList()
                    showPcDialog = true 
                }
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Computer, contentDescription = null)
                    Spacer(Modifier.width(12.dp))
                    Column(Modifier.weight(1f)) {
                        Text(
                            text = pairedPcId?.let { "已配对: $it" } ?: "未配对 PC",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Text(
                            text = "点击选择 PC",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
            
            Spacer(Modifier.height(16.dp))
            
            // 消息输入区域
            OutlinedTextField(
                value = messageText,
                onValueChange = { messageText = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                label = { Text("输入要发送给 Cursor 的需求...") },
                placeholder = { Text("例如：帮我实现一个登录页面") }
            )
            
            Spacer(Modifier.height(16.dp))
            
            // 发送按钮
            Button(
                onClick = {
                    if (messageText.isNotBlank() && pairedPcId != null) {
                        relayClient.sendToCursor(messageText)
                        messageText = ""
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = messageText.isNotBlank() && pairedPcId != null && connectionState == ConnectionState.CONNECTED
            ) {
                Icon(Icons.Default.Send, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("发送到 Cursor")
            }
        }
    }
    
    // PC 选择对话框
    if (showPcDialog) {
        AlertDialog(
            onDismissRequest = { showPcDialog = false },
            title = { Text("选择 PC") },
            text = {
                if (onlinePcs.isEmpty()) {
                    Text("暂无在线 PC，请确保 PC 端已启动")
                } else {
                    LazyColumn {
                        items(onlinePcs) { pcId ->
                            ListItem(
                                headlineContent = { Text(pcId) },
                                leadingContent = { Icon(Icons.Default.Computer, null) },
                                modifier = Modifier.fillMaxWidth(),
                                colors = ListItemDefaults.colors(
                                    containerColor = if (pcId == pairedPcId) 
                                        MaterialTheme.colorScheme.primaryContainer 
                                    else MaterialTheme.colorScheme.surface
                                )
                            )
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showPcDialog = false }) {
                    Text("关闭")
                }
            }
        )
    }
}
