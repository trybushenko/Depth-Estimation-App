import React, { useState } from 'react';
import styled from 'styled-components';
import { useDepthGPT } from '../hooks/useDepthGPT';
import DepthMapDisplay from './DepthMapDisplay';
import ErrorMessage from './ErrorMessage';

const PageContainer = styled.div`
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 20px;
`;

const ChatContainer = styled.div`
  margin-top: 20px;
`;

const ChatHistory = styled.div`
  max-height: 400px;
  overflow-y: auto;
  text-align: left;
  margin-bottom: 20px;
`;

const ChatMessage = styled.div<{ isUser: boolean }>`
  background-color: ${({ isUser }) => (isUser ? '#e0f7fa' : '#e8f5e9')};
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  max-width: 80%;
  align-self: ${({ isUser }) => (isUser ? 'flex-end' : 'flex-start')};
`;

const InputContainer = styled.div`
  display: flex;
`;

const TextInput = styled.input`
  flex: 1;
  padding: 10px;
  font-size: 16px;
`;

const SendButton = styled.button`
  padding: 10px;
  font-size: 16px;
`;

const FileInput = styled.input`
  margin-bottom: 20px;
`;

const DepthGPTPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prompt, setPrompt] = useState('');
  const {
    sendDepthGPTRequest,
    depthMap,
    rgbImage,
    lvlmResponse,
    chatHistory,
    loading,
    error,
  } = useDepthGPT();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSend = async () => {
    if (selectedFile && prompt) {
      await sendDepthGPTRequest(selectedFile, prompt);
      setPrompt('');
    }
  };

  return (
    <PageContainer>
      <Title>DepthGPT</Title>
      <FileInput type="file" accept="image/*" onChange={handleFileChange} />

      {rgbImage && (
        <div>
          <h3>Original Image</h3>
          <img src={`data:image/png;base64,${rgbImage}`} alt="Original" />
        </div>
      )}

      {depthMap && (
        <DepthMapDisplay depthMap={depthMap} />
      )}

      <ChatContainer>
        <ChatHistory>
          {chatHistory.map((message, index) => (
            <ChatMessage key={index} isUser={message.isUser}>
              {message.text}
            </ChatMessage>
          ))}
        </ChatHistory>
        <InputContainer>
          <TextInput
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your question..."
          />
          <SendButton onClick={handleSend} disabled={loading || !selectedFile || !prompt}>
            {loading ? 'Sending...' : 'Send'}
          </SendButton>
        </InputContainer>
      </ChatContainer>

      {error && <ErrorMessage>{error}</ErrorMessage>}
    </PageContainer>
  );
};

export default DepthGPTPage;
