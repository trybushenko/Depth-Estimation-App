// src/frontend/components/CameraStream.tsx

import React, { useRef, useEffect, useCallback } from 'react';
import Webcam from 'react-webcam';
import styled from 'styled-components';
import ErrorMessage from './ErrorMessage';

const WebcamContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
`;

const WebcamStyled = styled(Webcam)`
  width: 480px;
  height: 360px;
  border: 2px solid #2196f3;
  border-radius: 4px;
`;

interface CameraStreamProps {
  predictDepthFromFile: (file: File) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const CaptureInterval = 100; // Capture every 1000ms (1 second)

const CameraStream: React.FC<CameraStreamProps> = ({
  predictDepthFromFile,
  loading,
  error,
}) => {
  const webcamRef = useRef<Webcam>(null);

  // Function to convert base64 to Blob
  const base64ToBlob = (base64: string, mime: string) => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mime });
  };

  // Function to capture the current frame from the webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const [header, base64Image] = imageSrc.split(',');
        const mime = header.match(/:(.*?);/)?.[1] || 'image/png';
        const imageBlob = base64ToBlob(base64Image, mime);
        const imageFile = new File([imageBlob], 'captured_image.png', { type: mime });
        predictDepthFromFile(imageFile);
      }
    }
  }, [predictDepthFromFile]);

  // Capture a frame at regular intervals
  useEffect(() => {
    const interval = setInterval(() => {
      capture();
    }, CaptureInterval);

    return () => clearInterval(interval);
  }, [capture]);

  return (
    <div>
      <WebcamContainer>
        <WebcamStyled
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/png"
          videoConstraints={{
            width: 480,
            height: 360,
            facingMode: 'user',
          }}
        />
      </WebcamContainer>

      {/* Uncomment and implement LoadingSpinner if needed */}
      {/* {loading && <LoadingSpinner loading={loading} />} */}

      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};

export default CameraStream;
