export class GraphOathWebSocketClient {
  private url: string;
  private ws: WebSocket | null = null;
  private listeners: ((data: any) => void)[] = [];

  constructor(url: string = 'ws://localhost:8000/api/v1/ws/stream') {
    this.url = url;
  }

  public connect(): void {
    if (typeof window === 'undefined') return;
    try {
      this.ws = new WebSocket(this.url);
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.listeners.forEach((listener) => listener(data));
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };
      this.ws.onclose = () => {
        setTimeout(() => this.connect(), 3000);
      };
    } catch (e) {
      console.warn('WebSocket connection warning:', e);
    }
  }

  public subscribe(listener: (data: any) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }

  public send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}
