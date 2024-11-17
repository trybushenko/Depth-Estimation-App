// src/components/ImageUploader.tsx

import React, { useState } from 'react';
import { useDepthPrediction } from '../hooks/useDepthPrediction';
import { Input, Button, ErrorMessage } from './styles';

const ImageUploader: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { predictDepthFromFile, loading, error } = useDepthPrediction();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFile(e.target.files?.[0] || null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    await predictDepthFromFile(selectedFile);
  };

  return (
    <div>
      <Input type="file" accept="image/*" onChange={handleFileChange} />
      <Button onClick={handleUpload} disabled={!selectedFile || loading}>
        {loading ? 'Processing...' : 'Process'}
      </Button>
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};

export default ImageUploader;
