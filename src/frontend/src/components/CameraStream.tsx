// src/components/CameraStream.tsx

import React, { useRef, useEffect, useCallback } from 'react';
import Webcam from 'react-webcam';
import styled from 'styled-components';
// import LoadingSpinner from './LoadingSpinner';
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
  predictDepthFromBase64: (base64Image: string) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const CaptureInterval = 100; // Capture every 2000ms (2 seconds)

const CameraStream: React.FC<CameraStreamProps> = ({
  predictDepthFromBase64,
  loading,
  error,
}) => {
  const webcamRef = useRef<Webcam>(null);

  // Function to capture the current frame from the webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        // Remove the data URL prefix to get the base64 string
        const base64Image = imageSrc.split(',')[1];
        predictDepthFromBase64(base64Image);
      }
    }
  }, [predictDepthFromBase64]);

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

      {/* {loading && <LoadingSpinner loading={loading} />} */}

      {error && <ErrorMessage>{error}</ErrorMessage>}
    </div>
  );
};

export default CameraStream;
