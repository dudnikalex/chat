import React from 'react';
import './components.scss';

const ChatMessage = (props) => {
    const messageType = 'chat-message' + (props.own ? '-own' : '');
    return (
        <div className={'chat-message ' + messageType}>{props.children}</div>
    );
};

export default ChatMessage;
