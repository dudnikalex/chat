import React, { Component, useState } from 'react';
import './chat.scss';

import ChatMessage from '../../components/message';
import RoundButton from '../../components/round-button';
import TextInput from '../../components/text-input';
import ConfusingGlobals from 'confusing-browser-globals';

export default class Chat extends Component {
    constructor(props) {
        super(props);

        this.state = {
            messages: [],
        };

        this.appendMessage = this.appendMessage.bind(this);
        this.onMessageSend = this.onMessageSend.bind(this);
    }

    componentDidMount() {
        this.socket = new WebSocket('ws://0.0.0.0:8000/ws/');
        this.socket.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            msg.own = false;
            if (msg.type == 'text') {
                // console.log('received text message');
                this.appendMessage(msg);
            }

            if (msg.type == 'disconnect') {
                this.setState({ messages: [] });
                alert('user disconnected');
            }

            if (msg.type == 'connectedmessage') {
                alert('user connected');
            }
        };
    }

    appendMessage(message) {
        // console.log('states', this.state.items);
        this.setState((state) => {
            return {
                messages: state.messages.concat([message]),
            };
        });
    }

    onMessageSend(text) {
        // this.socket.send()
        const msg = { text: text, own: true };
        this.socket.send(text);
        this.appendMessage(msg);
    }

    render() {
        return (
            <div>
                <div className="header">
                    <RoundButton
                        onClick={() => {
                            alert('not implemented!');
                        }}
                        color="#f74336">
                        END CHAT
                    </RoundButton>
                </div>

                <div className="wrap">
                    {this.state.messages.map((message, index) => {
                        return (
                            <ChatMessage key={index} own={message.own}>
                                {message.text}
                            </ChatMessage>
                        );
                    })}
                </div>

                <div className="bottom">
                    <TextInput onSubmit={this.onMessageSend}></TextInput>
                </div>
            </div>
        );
    }
}
