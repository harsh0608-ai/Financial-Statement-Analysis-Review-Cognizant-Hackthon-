"use client";

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { WavyBackground } from "./components/ui/wavy-background";
import { 
  ArrowLeft, 
  BarChart2,
  Code, 
  AlertTriangle, 
  Info, 
  AlertCircle,
  Upload,
  Table as TableIcon
} from "lucide-react";

export default function TableReportPage() {
  const [reportData, setReportData] = useState(null);
  const navigate = useNavigate();
const handleDownloadHTML = () => {
  if (!reportData) return;

  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audit Report - ${reportData.statement || "Financial Statement"}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0d0d0d; color: #e5e5e5; padding: 40px; margin: 0; }
    .container { max-width: 1100px; margin: 0 auto; background: #171717; padding: 32px; border-radius: 16px; border: 1px solid #262626; }
    h1 { font-size: 24px; color: #ffffff; margin-bottom: 4px; }
    .subtitle { color: #a3a3a3; font-size: 14px; margin-bottom: 24px; }
    .summary-box { background: #262626; border-left: 4px solid #3b82f6; padding: 16px; border-radius: 8px; margin-bottom: 32px; line-height: 1.6; }
    table { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 14px; }
    th { background-color: #262626; color: #d4d4d4; text-align: left; padding: 12px; border-bottom: 2px solid #404040; }
    td { padding: 12px; border-bottom: 1px solid #262626; color: #a3a3a3; }
    tr:hover { background-color: #1f1f1f; }
    .badge { padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; display: inline-block; }
    .badge-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-medium { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-low { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .mono { font-family: monospace; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Audit Analysis Report</h1>
    <p class="subtitle">Statement: <strong>${reportData.statement || "N/A"}</strong></p>
    
    ${reportData.summary ? `
      <div class="summary-box">
        <strong style="color: #ffffff;">Executive Summary:</strong><br/>
        ${reportData.summary}
      </div>
    ` : ""}

    <h2>Audit Findings</h2>
    <table>
      <thead>
        <tr>
          <th>Severity</th>
          <th>Location</th>
          <th>Check Type</th>
          <th>Reported</th>
          <th>Expected</th>
          <th>Difference</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        ${reportData.findings.map(f => {
          const sev = (f.severity || "info").toLowerCase();
          const badgeClass = sev === "high" ? "badge-high" : sev === "medium" ? "badge-medium" : "badge-low";
          
          return `
            <tr>
              <td><span class="badge ${badgeClass}">${f.severity || "Info"}</span></td>
              <td style="color: #ffffff;">${f.location || "-"}</td>
              <td>${(f.checkType || "-").replace(/_/g, " ")}</td>
              <td class="mono">${f.reported ? `$${f.reported}` : "-"}</td>
              <td class="mono">${f.expected ? `$${f.expected}` : "-"}</td>
              <td class="mono">${f.difference ? `$${f.difference}` : "-"}</td>
              <td>${f.description || "-"}</td>
            </tr>
          `;
        }).join("")}
      </tbody>
    </table>
  </div>
</body>
</html>
  `;

  const blob = new Blob([htmlContent], { type: "text/html;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `Audit_Report_${reportData.statement || "Export"}.html`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
  useEffect(() => {
    const savedData = localStorage.getItem("auditReportData");
    if (savedData) {
      try {
        setReportData(JSON.parse(savedData));
      } catch (err) {
        console.error("Failed to parse audit data from localStorage", err);
      }
    }
  }, []);

  const getSeverityBadge = (severity) => {
    switch (severity?.toLowerCase()) {
      case "high":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/20"><AlertCircle className="w-3 h-3" /> High</span>;
      case "medium":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20"><AlertTriangle className="w-3 h-3" /> Medium</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20"><Info className="w-3 h-3" /> Info</span>;
    }
  };

  if (!reportData) {
    return (
      <WavyBackground className="max-w-5xl mx-auto pb-20 px-4 min-h-screen flex flex-col justify-center items-center text-center">
        <div className="p-8 rounded-3xl bg-neutral-900/70 border border-neutral-800 backdrop-blur-md max-w-lg w-full flex flex-col items-center">
          <div className="w-16 h-16 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-4 text-blue-400">
            <TableIcon className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">No Report Data Available</h2>
          <p className="text-neutral-400 text-sm mb-6">
            Please upload a financial statement first to generate the audit report table.
          </p>
          <button
            onClick={() => navigate("/upload")}
            className="flex items-center gap-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl transition-colors shadow-lg"
          >
            <Upload className="w-4 h-4" /> Go to Upload Page
          </button>
        </div>
      </WavyBackground>
    );
  }

  return (
    <WavyBackground className="max-w-7xl mx-auto pb-20 px-4 min-h-screen flex flex-col items-center">
      <div className="w-full mt-10 flex flex-col items-start gap-6">
        
        {/* Navigation Actions Header */}
<div className="w-full flex flex-wrap justify-between items-center gap-4">
  <button
    onClick={() => navigate("/upload")}
    className="flex items-center gap-2 text-sm text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 px-4 py-2 rounded-xl transition-colors border border-neutral-800 backdrop-blur-md cursor-pointer"
  >
    <ArrowLeft className="w-4 h-4" /> Upload Another File
  </button>
  
  <div className="flex items-center gap-3">
    <button
      onClick={handleDownloadHTML}
      className="flex items-center gap-2 text-sm font-medium text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 px-4 py-2 rounded-xl transition-colors border border-neutral-800 backdrop-blur-md cursor-pointer"
    >
      <Code className="w-4 h-4 text-blue-400" /> Export HTML
    </button>

    <button
      onClick={() => navigate("/dash")}
      className="flex items-center gap-2 text-sm font-medium text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 px-4 py-2 rounded-xl transition-colors border border-neutral-800 backdrop-blur-md cursor-pointer"
    >
      <BarChart2 className="w-4 h-4" /> View Visual Dashboard
    </button>
  </div>
</div>

        {/* Top Header Card */}
        <div className="w-full bg-neutral-900/70 border border-neutral-800 rounded-2xl p-6 backdrop-blur-md shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
              {reportData.title}
            </h1>
            <p className="text-neutral-400 text-sm mt-1">
              Statement: <span className="text-blue-400 font-medium">{reportData.statement}</span>
            </p>
          </div>

          <div className="flex items-center gap-6 text-sm text-neutral-400 border-t md:border-t-0 md:border-l border-neutral-800 pt-3 md:pt-0 md:pl-6">
            <div>
              <p className="text-xs text-neutral-500 uppercase tracking-wider font-semibold">Generated</p>
              <p className="text-neutral-200 mt-0.5">{reportData.generated}</p>
            </div>
            <div>
              <p className="text-xs text-neutral-500 uppercase tracking-wider font-semibold">Total Findings</p>
              <p className="text-red-400 font-bold text-base mt-0.5">{reportData.totalFindings}</p>
            </div>
          </div>
        </div>

        {/* Full Table */}
        <div className="w-full bg-neutral-900/80 border border-neutral-800 rounded-2xl overflow-hidden shadow-2xl backdrop-blur-md">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs md:text-sm">
              <thead>
                <tr className="bg-neutral-950/80 border-b border-neutral-800 text-neutral-400 uppercase text-[11px] font-semibold tracking-wider">
                  <th className="py-3.5 px-4">Check Type</th>
                  <th className="py-3.5 px-4">Location</th>
                  <th className="py-3.5 px-4">Severity</th>
                  <th className="py-3.5 px-4">Description</th>
                  <th className="py-3.5 px-4">Reported</th>
                  <th className="py-3.5 px-4">Expected</th>
                  <th className="py-3.5 px-4">Difference</th>
                  <th className="py-3.5 px-4">Explanation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-800/60 text-neutral-300">
                {reportData.findings.map((item, index) => (
                  <tr key={index} className="hover:bg-neutral-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono text-neutral-300">{item.checkType}</td>
                    <td className="py-3 px-4 font-medium text-white">{item.location}</td>
                    <td className="py-3 px-4 whitespace-nowrap">{getSeverityBadge(item.severity)}</td>
                    <td className="py-3 px-4 max-w-xs text-neutral-300">{item.description}</td>
                    <td className="py-3 px-4 font-mono">{item.reported}</td>
                    <td className="py-3 px-4 font-mono">{item.expected}</td>
                    <td className="py-3 px-4 font-mono text-amber-400">{item.difference}</td>
                    <td className="py-3 px-4 max-w-xs text-neutral-400">{item.explanation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </WavyBackground>
  );
}