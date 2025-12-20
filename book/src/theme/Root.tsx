import React from 'react';
import Chatbot from '../components/Chatbot/Chatbot';

export default function Root({ children }) {
  console.log('Root component rendering');
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}