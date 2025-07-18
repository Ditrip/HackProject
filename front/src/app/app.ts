import { Component, ElementRef, ViewChild, AfterViewChecked, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ApiService } from './api.service';

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
  private apiService = inject(ApiService);

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
    console.log('START');
    // this.apiService.getData();
    // Simulate AI response
    this.AIResponse(userMessage.content);
  }

  private AIResponse(userInput: string) {
    this.isTyping = true;
    this.shouldScrollToBottom = true;

    this.apiService.sendQuery(userInput).subscribe({
      next: (response: any) => {
        let rawText: string = '';

        if (typeof response === 'string') {
          rawText = response;
        } else if (response?.answer) {
          rawText = String(response.answer);
        } else if (response?.message) {
          rawText = String(response.message);
        } else {
          rawText = JSON.stringify(response, null, 2);
        }
        
        const safeText: string = String(rawText);

        const formattedResponse = safeText
          .replace(/\n/g, '<br>')
          .replace(
            /(https?:\/\/\S+)/g,
            '<a href="$1" target="_blank">$1</a>'
          );

        const assistantMessage: Message = {
          id: this.messageIdCounter++,
          role: 'assistant',
          content: formattedResponse,
          timestamp: new Date(),
        };

        this.messages.push(assistantMessage);
        this.isTyping = false;
        this.shouldScrollToBottom = true;
      },
      error: err => {
        console.error('API Error:', err);
        this.isTyping = false;
      }
    });
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
