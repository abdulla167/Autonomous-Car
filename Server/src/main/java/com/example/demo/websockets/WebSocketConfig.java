package com.example.demo.websockets;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;


@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Autowired
    ApplicationContext context;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry webSocketHandlerRegistry) {
        webSocketHandlerRegistry.addHandler(context.getBean("espSocket", EspSocket.class), "/esp")
                .setAllowedOrigins("*");
        webSocketHandlerRegistry.addHandler(context.getBean("controllerSocket", ControllerSocket.class), "/control")
                .setAllowedOrigins("*");
    }

}

