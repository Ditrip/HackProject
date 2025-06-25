import { Component, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule, CommonModule, ButtonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
  standalone: true,
})
export class App implements AfterViewChecked {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('messageInput') messageInput!: ElementRef;

  messages: Message[] = [];
  currentMessage = '';
  isTyping = false;
  private messageIdCounter = 1;
  private shouldScrollToBottom = false;

  ngAfterViewChecked() {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  sendMessage() {
    if (!this.currentMessage.trim() || this.isTyping) {
      return;
    }

    // Add user message
    const userMessage: Message = {
      id: this.messageIdCounter++,
      role: 'user',
      content: this.currentMessage.trim(),
      timestamp: new Date(),
    };

    this.messages.push(userMessage);
    this.currentMessage = '';
    this.shouldScrollToBottom = true;

    // Reset textarea height
    if (this.messageInput?.nativeElement) {
      this.messageInput.nativeElement.style.height = 'auto';
    }

    // Simulate AI response
    this.simulateAIResponse(userMessage.content);
  }

  private simulateAIResponse(userInput: string) {
    this.isTyping = true;
    this.shouldScrollToBottom = true;

    // Simulate typing delay
    setTimeout(
      () => {
        const responses = [
          'I understand your question. Let me help you with that.',
          "That's an interesting point. Here's what I think about it...",
          "I'd be happy to assist you with that. Based on what you've asked...",
          'Great question! Let me break this down for you.',
          "I can help you with that. Here's my response to your inquiry.",
          "Thank you for your message. Here's what I can tell you about that topic.",
          "That's a thoughtful question. Let me provide you with some insights.",
          "I appreciate you asking. Here's my take on what you've mentioned.",
        ];

        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        const assistantMessage: Message = {
          id: this.messageIdCounter++,
          role: 'assistant',
          content: randomResponse + ' ' + this.generateContextualResponse(userInput),
          timestamp: new Date(),
        };

        this.messages.push(assistantMessage);
        this.isTyping = false;
        this.shouldScrollToBottom = true;
      },
      1000 + Math.random() * 2000
    ); // Random delay between 1-3 seconds
  }

  private generateContextualResponse(userInput: string): string {
    return "Hello! It's great to meet you. How can I assist you today?";
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  adjustTextareaHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    const maxHeight = 200; // Maximum height in pixels
    const newHeight = Math.min(textarea.scrollHeight, maxHeight);
    textarea.style.height = newHeight + 'px';
  }

  clearChat() {
    this.messages = [];
    this.currentMessage = '';
    this.isTyping = false;
  }

  private scrollToBottom() {
    if (this.messagesContainer?.nativeElement) {
      const container = this.messagesContainer.nativeElement;
      container.scrollTop = container.scrollHeight;
    }
  }
}
