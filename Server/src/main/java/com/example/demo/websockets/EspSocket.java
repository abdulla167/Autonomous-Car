package com.example.demo.websockets;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;


@Component
public class EspSocket extends TextWebSocketHandler {

    private WebSocketSession _session;

    @Autowired
    ApplicationContext context;

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        System.out.println(message.getPayload());
        try{
            context.getBean("controllerSocket", ControllerSocket.class).getSession().sendMessage(message);
        } catch (Exception e){
            System.out.println("Not Sent to Mobile");
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("esp connected");
        _session = session;
    }

    public WebSocketSession getSession() {
        return _session;
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("esp disconnected");
    }
}
