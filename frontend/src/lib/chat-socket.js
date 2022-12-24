class ChatWSHandler {
    constructor(url) {
        this.ws = new WebSocket(url);
    }
}
