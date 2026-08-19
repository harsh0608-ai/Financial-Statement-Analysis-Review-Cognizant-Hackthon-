"use client";

import React from "react";
import "./index.css";
import { TypewriterText } from "./components/TypewriterText";

import { WavyBackground } from "./components/ui/wavy-background";
import { useNavigate } from "react-router-dom";

const heroLines = [
  "Welcome to FinReview,",
  "where your financial needs",
  "can be taken care of",
  "with a simple click.",
];
export default function AboutUs() {
    const navigate = useNavigate();
  return (
    <WavyBackground className="max-w-4xl mx-auto pb-40">

      <div className="pt-32">

        {/* Typewriter */}
        <div className="w-full flex justify-center">
          <div className="w-[900px] max-w-full">
            <TypewriterText
              lines={heroLines}
              speed={40}
              pause={1200}
              className="w-full text-3xl md:text-6xl font-bold text-white text-center tracking-tight"
            />
          </div>
        </div>

        {/* Other text */}
        <p className="text-base md:text-lg mt-4 text-white font-normal inter-var text-center">
          Are you ready?
        </p>

        {/* Button */}
        <div className="w-full flex justify-center mt-6">
          <button onClick={() => navigate("/upload")}
 className="p-[3px] relative">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />

            <div className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white hover:bg-transparent">
              Get Started
            </div>
          </button>
        </div>

      </div>

    </WavyBackground>
  );
}

