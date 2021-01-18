package com.example.demo.websockets;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.BinaryWebSocketHandler;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.util.List;
import java.util.Random;

@Component
public class ImageSocket extends BinaryWebSocketHandler {

    @Autowired
    ApplicationContext context;

    @Override
    public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws Exception {
       /* List<WebSocketSession> sessions = context.getBean("dispatcherHandler", DispatcherHandler.class).getSessions();
        for (WebSocketSession s : sessions){
            s.sendMessage(new TextMessage(Integer.toString(new Random().nextInt())));
        }*/
        System.out.println(message.toString());

    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("connected");
        session.setTextMessageSizeLimit(1024 * 1024); // 1Mb
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        System.out.println("error");
        exception.printStackTrace();
        session.close();
    }
}
