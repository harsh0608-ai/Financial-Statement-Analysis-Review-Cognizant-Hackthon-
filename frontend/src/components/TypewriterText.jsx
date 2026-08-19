import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

export function TypewriterText({ lines, speed = 50, pause = 2000, className = "" }) {
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState("");
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    const currentFullText = lines[currentLineIndex];

    if (isTyping) {
      if (displayedText.length < currentFullText.length) {
        const timeout = setTimeout(() => {
          setDisplayedText(currentFullText.slice(0, displayedText.length + 1));
        }, speed);
        return () => clearTimeout(timeout);
      } else {
        // Line fully typed out, pause before clearing
        const timeout = setTimeout(() => {
          setIsTyping(false);
        }, pause);
        return () => clearTimeout(timeout);
      }
    } else {
      // Transition to next line
      setDisplayedText("");
      setCurrentLineIndex((prev) => (prev + 1) % lines.length);
      setIsTyping(true);
    }
  }, [displayedText, isTyping, currentLineIndex, lines, speed, pause]);

  return (
    <div className={`relative min-h-[1.5em] flex items-center justify-center ${className}`}>
      <AnimatePresence mode="wait">
        <motion.span
          key={currentLineIndex}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
          className="inline-block"
        >
          {displayedText}
          <motion.span
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.6, repeat: Infinity, repeatType: "reverse" }}
            className="inline-block ml-1 w-[3px] h-[0.9em] bg-white align-middle"
          />
        </motion.span>
      </AnimatePresence>
    </div>
  );
}