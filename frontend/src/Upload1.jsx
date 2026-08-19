"use client";

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { WavyBackground } from "./components/ui/wavy-background";
import {
  Upload,
  CheckCircle2,
  ShieldCheck,
  FileCheck,
  FileSpreadsheet,
  Loader2,
} from "lucide-react";

// Main backend API
const API_BASE_URL = "http://127.0.0.1:8000";

/*
 * Upload the financial statement to the backend,
 * wait for the audit pipeline to finish,
 * then retrieve the generated findings.
 */
async function processFileWithBackend(file) {
  // --------------------------------------------------
  // 1. Upload the PDF
  // --------------------------------------------------
  const formData = new FormData();
  formData.append("file", file);

  const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!uploadResponse.ok) {
    const errorText = await uploadResponse.text();
    throw new Error(
      `Upload failed (${uploadResponse.status}): ${errorText}`
    );
  }

  const uploadData = await uploadResponse.json();

  console.log("Upload response:", uploadData);

  const statementId = uploadData.id;

  if (!statementId) {
    throw new Error("Backend did not return a statement ID.");
  }

  // --------------------------------------------------
  // 2. Poll backend until processing is complete
  // --------------------------------------------------
  let statusData;

  while (true) {
    const statusResponse = await fetch(
      `${API_BASE_URL}/status/${statementId}`
    );

    if (!statusResponse.ok) {
      const errorText = await statusResponse.text();
      throw new Error(
        `Status check failed (${statusResponse.status}): ${errorText}`
      );
    }

    statusData = await statusResponse.json();

    console.log("Pipeline status:", statusData);

    if (statusData.status === "done") {
      break;
    }

    if (statusData.status === "failed") {
      throw new Error(
        "Financial statement processing failed on the backend."
      );
    }

    // Wait 1.5 seconds before checking again
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }

  // --------------------------------------------------
  // 3. Retrieve actual findings from backend
  // --------------------------------------------------
  const findingsResponse = await fetch(
    `${API_BASE_URL}/findings/${statementId}`
  );

  if (!findingsResponse.ok) {
    const errorText = await findingsResponse.text();
    throw new Error(
      `Failed to fetch findings (${findingsResponse.status}): ${errorText}`
    );
  }

  const findingsData = await findingsResponse.json();

  console.log("Findings response:", findingsData);

  // --------------------------------------------------
  // 4. Convert backend response into the format
  //    expected by the existing Table/Dashboard pages
  // --------------------------------------------------
  const parsedReport = {
    title: "Financial Statement Audit Report",
    statement: statusData.filename || file.name,
    generated: new Date().toISOString(),
    totalFindings: findingsData.count || findingsData.findings?.length || 0,

    findings: (findingsData.findings || []).map((finding) => ({
      id: finding.id,

      checkType: finding.check_type || "-",
      location: finding.location || "-",
      severity: finding.severity || "-",
      description: finding.description || "-",

      reported:
        finding.reported_value !== null &&
        finding.reported_value !== undefined
          ? finding.reported_value
          : "-",

      expected:
        finding.expected_value !== null &&
        finding.expected_value !== undefined
          ? finding.expected_value
          : "-",

      difference:
        finding.difference !== null &&
        finding.difference !== undefined
          ? finding.difference
          : "-",

      explanation: finding.explanation || "-",
    })),
  };

  return parsedReport;
}

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const navigate = useNavigate();

  // --------------------------------------------------
  // Handle PDF selection/upload
  // --------------------------------------------------
  const handleFileChange = async (e) => {
    if (!e.target.files || !e.target.files[0]) {
      return;
    }

    const file = e.target.files[0];

    // Only allow PDFs
    if (file.type !== "application/pdf") {
      alert("Please upload a financial statement PDF.");
      return;
    }

    // 50 MB limit
    const maxSize = 50 * 1024 * 1024;

    if (file.size > maxSize) {
      alert("File size must be less than 50 MB.");
      return;
    }

    setSelectedFile(file);
    setIsProcessing(true);

    try {
      console.log("Uploading:", file.name);

      const parsedReport = await processFileWithBackend(file);

      console.log("Final audit report:", parsedReport);

      // Save actual backend results for Table/Dashboard pages
      localStorage.setItem(
        "auditReportData",
        JSON.stringify(parsedReport)
      );

      // Navigate to findings table
      navigate("/table");
    } catch (error) {
      console.error(
        "Error processing financial statement:",
        error
      );

      alert(
        `Processing failed:\n\n${error.message}`
      );
    } finally {
      setIsProcessing(false);
    }
  };

  // --------------------------------------------------
  // Clear previous audit data
  // --------------------------------------------------
  const handleClearStorage = () => {
    localStorage.removeItem("auditReportData");
    setSelectedFile(null);
    setIsProcessing(false);
  };

  return (
    <WavyBackground className="max-w-4xl mx-auto px-4 min-h-screen flex flex-col items-center">
      <div className="w-full flex flex-col items-center justify-center flex-1 py-20">

        {/* Header */}
        <p className="text-3xl md:text-5xl lg:text-6xl text-white font-bold text-center tracking-tight">
          Financial Statement Audit AI
        </p>

        <p className="text-base md:text-lg mt-3 text-neutral-300 font-normal text-center max-w-xl">
          Upload your statements below to perform automated
          reconciliation, variance detection, and rule validation.
        </p>

        {/* Upload Box */}
        <div className="w-full mt-10 p-8 rounded-3xl bg-neutral-900/60 backdrop-blur-md border border-dashed border-neutral-700/80 hover:border-neutral-500 transition-all duration-300 shadow-2xl relative group">

          <label className="flex flex-col items-center justify-center cursor-pointer w-full py-6">

            <input
              type="file"
              className="hidden"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              disabled={isProcessing}
            />

            {/* Upload Icon */}
            <div className="w-16 h-16 rounded-full bg-white/10 group-hover:bg-white/20 border border-white/10 flex items-center justify-center mb-5 transition-transform duration-300 group-hover:scale-105">

              {isProcessing ? (
                <Loader2 className="w-7 h-7 text-blue-400 animate-spin" />
              ) : (
                <Upload className="w-7 h-7 text-white" />
              )}

            </div>

            {/* Upload Status */}
            <h3 className="text-xl md:text-2xl font-semibold text-white text-center">

              {isProcessing ? (
                <span className="text-blue-400">
                  Processing financial document...
                </span>
              ) : selectedFile ? (
                <span className="text-blue-400">
                  {selectedFile.name}
                </span>
              ) : (
                "Upload your Financial Statements here"
              )}

            </h3>

            {/* Browse Text */}
            {!selectedFile && !isProcessing && (
              <p className="text-sm md:text-base text-neutral-400 mt-2 text-center">
                or{" "}
                <span className="text-blue-400 font-medium underline underline-offset-4 hover:text-blue-300 transition-colors">
                  browse from your computer
                </span>
              </p>
            )}

            {/* File Information */}
            <p className="text-xs text-neutral-500 mt-4 text-center">
              Supports financial statement PDF (Max 50MB)
            </p>

          </label>
        </div>

        <div className="w-full h-[1px] bg-neutral-800 my-10" />

        {/* Features Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full">

          {/* Math Accuracy */}
          <div className="flex flex-col items-center text-center">

            <div className="w-10 h-10 rounded-xl bg-neutral-900/80 border border-neutral-800 flex items-center justify-center mb-3">
              <CheckCircle2 className="w-5 h-5 text-white" />
            </div>

            <h4 className="text-sm font-semibold text-white">
              Math Accuracy
            </h4>

            <p className="text-xs text-neutral-400 mt-1">
              Reconcile cross-totals
            </p>

          </div>

          {/* Prior Year */}
          <div className="flex flex-col items-center text-center">

            <div className="w-10 h-10 rounded-xl bg-neutral-900/80 border border-neutral-800 flex items-center justify-center mb-3">
              <ShieldCheck className="w-5 h-5 text-white" />
            </div>

            <h4 className="text-sm font-semibold text-white">
              Prior Year Tie Out
            </h4>

            <p className="text-xs text-neutral-400 mt-1">
              Match opening balances
            </p>

          </div>

          {/* Consistency */}
          <div className="flex flex-col items-center text-center">

            <div className="w-10 h-10 rounded-xl bg-neutral-900/80 border border-neutral-800 flex items-center justify-center mb-3">
              <FileCheck className="w-5 h-5 text-white" />
            </div>

            <h4 className="text-sm font-semibold text-white">
              Consistency & Grammar
            </h4>

            <p className="text-xs text-neutral-400 mt-1">
              Spelling & logic checks
            </p>

          </div>

          {/* WP-514 */}
          <div className="flex flex-col items-center text-center">

            <div className="w-10 h-10 rounded-xl bg-neutral-900/80 border border-neutral-800 flex items-center justify-center mb-3">
              <FileSpreadsheet className="w-5 h-5 text-white" />
            </div>

            <h4 className="text-sm font-semibold text-white">
              WP-514 Analytics
            </h4>

            <p className="text-xs text-neutral-400 mt-1">
              Auto-populated working papers
            </p>

          </div>

        </div>
      </div>

      {/* Clear Saved Data */}
      <button
        onClick={handleClearStorage}
        className="mt-10 mb-10 flex items-center gap-2 text-sm text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-red-900/40 px-4 py-2 rounded-xl transition-colors border border-neutral-800 hover:border-red-800 backdrop-blur-md cursor-pointer"
      >
        Clear Saved Audit Data
      </button>

    </WavyBackground>
  );
}