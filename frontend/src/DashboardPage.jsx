"use client";

import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { WavyBackground } from "./components/ui/wavy-background";
import { 
  ArrowLeft, 
  AlertTriangle, 
  FilePieChart, 
  TrendingUp, 
  ShieldAlert,
  BarChart3,
  Upload,
  Download,
  Loader2,
  Table as TableIcon
} from "lucide-react";
import { 
  PieChart, 
  Pie, 
  Cell, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid
} from "recharts";
import html2canvas from "html2canvas-pro";
import jsPDF from "jspdf";

const CustomBarTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;

    return (
      <div className="bg-neutral-900 border border-neutral-700 p-3 rounded-xl shadow-2xl text-xs max-w-sm pointer-events-none z-50">
        <p className="font-semibold text-white mb-2 border-b border-neutral-800 pb-1">
          {data.fullLocation || data.name}
        </p>
        {data.Discrepancy !== undefined && (
          <p className="text-amber-400 font-mono">
            Discrepancy: <span className="font-bold">${data.Discrepancy.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </p>
        )}
        {data.Reported !== undefined && (
          <p className="text-red-400 font-mono">
            Reported: <span className="font-bold">${data.Reported.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </p>
        )}
        {data.Expected !== undefined && (
          <p className="text-emerald-400 font-mono">
            Expected: <span className="font-bold">${data.Expected.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </p>
        )}
        {data.count !== undefined && (
          <p className="text-blue-400 font-mono">
            Total Issues: <span className="font-bold">{data.count}</span>
          </p>
        )}
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  const [reportData, setReportData] = useState(null);
  const [isExporting, setIsExporting] = useState(false);
  const navigate = useNavigate();
  const dashboardRef = useRef(null);

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

  const handleDownloadPDF = async () => {
    if (!dashboardRef.current) return;
    setIsExporting(true);

    try {
      const element = dashboardRef.current;
      const canvas = await html2canvas(element, {
        scale: 2,
        backgroundColor: "#0a0a0a",
        useCORS: true
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

      pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Audit_Analytics_${reportData?.statement || "Report"}.pdf`);
    } catch (error) {
      console.error("Error generating PDF:", error);
    } finally {
      setIsExporting(false);
    }
  };

  if (!reportData || !reportData.findings || reportData.findings.length === 0) {
    return (
      <WavyBackground className="max-w-5xl mx-auto pb-20 px-4 min-h-screen flex flex-col justify-center items-center text-center">
        <div className="p-8 rounded-3xl bg-neutral-900/70 border border-neutral-800 backdrop-blur-md max-w-lg w-full flex flex-col items-center">
          <div className="w-16 h-16 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-4 text-blue-400">
            <BarChart3 className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">No Audit Data Found</h2>
          <p className="text-neutral-400 text-sm mb-6">
            Please upload a financial statement first to generate visual analytics.
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

  // --- DATA TRANSFORMATIONS ---
  const severityCounts = reportData.findings.reduce((acc, curr) => {
    const sev = curr.severity ? curr.severity.toLowerCase() : "info";
    acc[sev] = (acc[sev] || 0) + 1;
    return acc;
  }, {});

  const severityData = [
    { name: "High", value: severityCounts.high || 0, color: "#ef4444" },
    { name: "Medium", value: severityCounts.medium || 0, color: "#f59e0b" },
    { name: "Low / Info", value: severityCounts.low || severityCounts.info || 0, color: "#3b82f6" },
  ].filter(d => d.value > 0);

  const checkTypeCounts = reportData.findings.reduce((acc, curr) => {
    const type = curr.checkType || "Other";
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {});

  const checkTypeData = Object.keys(checkTypeCounts).map(key => ({
    name: key.replace(/_/g, " "),
    count: checkTypeCounts[key]
  }));

  // Aggregate duplicate findings by unique location name
 const aggregatedMap = {};

reportData.findings.forEach(f => {
  const loc = f.location || "Unknown Location";
  const rep = parseFloat(f.reported);
  const exp = parseFloat(f.expected);
  const diff = parseFloat(f.difference);

  const discrepancyValue = !isNaN(diff) 
    ? Math.abs(diff) 
    : (!isNaN(rep) && !isNaN(exp) ? Math.abs(rep - exp) : 0);

  if (discrepancyValue > 0) {
    if (!aggregatedMap[loc]) {
      aggregatedMap[loc] = {
        fullLocation: loc,
        Discrepancy: discrepancyValue,
        Reported: isNaN(rep) ? undefined : rep,
        Expected: isNaN(exp) ? undefined : exp,
        count: 1
      };
    } else {
      aggregatedMap[loc].Discrepancy = Math.max(aggregatedMap[loc].Discrepancy, discrepancyValue);
      aggregatedMap[loc].count += 1;
    }
  }
});

const largestDiscrepanciesData = Object.values(aggregatedMap)
  .sort((a, b) => b.Discrepancy - a.Discrepancy)
  .slice(0, 5)
  .map((item, index) => ({
    ...item,
    // Unique key ensures Recharts creates distinct bar slots
    chartKey: `location_slot_${index}`
  }));

  const totalVariance = largestDiscrepanciesData.reduce((sum, item) => sum + item.Discrepancy, 0);

  return (
    <WavyBackground className="max-w-7xl mx-auto pb-20 px-4 min-h-screen flex flex-col items-center">
      {/* Navigation Header */}
      <div className="w-full mt-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">

    {/* Left: Back button + title */}
    <div className="flex items-center gap-4">
      <button
        onClick={() => navigate("/table")}
        className="flex items-center gap-2 text-sm text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 px-4 py-2 rounded-xl transition-colors border border-neutral-800 backdrop-blur-md cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Table
      </button>

      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
          Audit Visual Dashboard
        </h1>
        <p className="text-neutral-400 text-xs md:text-sm">
          Statement:{" "}
          <span className="text-blue-400 font-medium">
            {reportData.statement}
          </span>
        </p>
      </div>
    </div>

    {/* Right: Download button */}
    <button
      onClick={handleDownloadPDF}
      disabled={isExporting}
      className="flex items-center gap-2 text-sm text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 px-4 py-2 rounded-xl transition-colors border border-neutral-800 backdrop-blur-md cursor-pointer"
    >
      {isExporting ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin" />
          Generating PDF...
        </>
      ) : (
        <>
          <Download className="w-4 h-4" />
          Download Charts as PDF
        </>
      )}
    </button>

  </div>

      {/* Capture Area for PDF Download */}
      <div ref={dashboardRef} className="w-full mt-6 flex flex-col gap-6 p-2">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full">
          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-5 backdrop-blur-md flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Total Findings</p>
              <p className="text-2xl font-bold text-white mt-1">{reportData.totalFindings || reportData.findings.length}</p>
            </div>
            <div className="p-3 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-xl">
              <FilePieChart className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-5 backdrop-blur-md flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">High Risk Issues</p>
              <p className="text-2xl font-bold text-red-400 mt-1">{severityCounts.high || 0}</p>
            </div>
            <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl">
              <ShieldAlert className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-5 backdrop-blur-md flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Medium Risk Issues</p>
              <p className="text-2xl font-bold text-amber-400 mt-1">{severityCounts.medium || 0}</p>
            </div>
            <div className="p-3 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-xl">
              <AlertTriangle className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-5 backdrop-blur-md flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Top 5 Variance Sum</p>
              <p className="text-2xl font-bold text-amber-400 mt-1">${totalVariance.toLocaleString(undefined, { minimumFractionDigits: 2 })}</p>
            </div>
            <div className="p-3 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-xl">
              <TrendingUp className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
          {/* Chart 1 */}
          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-6 backdrop-blur-md flex flex-col justify-between">
            <h3 className="text-lg font-semibold text-white mb-2">Findings Severity Distribution</h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={severityData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {severityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomBarTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2 */}
          <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-6 backdrop-blur-md flex flex-col justify-between">
            <h3 className="text-lg font-semibold text-white mb-2">Issues by Check Category</h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={checkTypeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
                  <XAxis dataKey="name" stroke="#a3a3a3" fontSize={11} />
                  <YAxis stroke="#a3a3a3" fontSize={11} />
                  <Tooltip content={<CustomBarTooltip />} cursor={{ fill: "rgba(255, 255, 255, 0.05)" }} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 3: Aggregated Unique Entries */}
          {largestDiscrepanciesData.length > 0 && (
  <div className="bg-neutral-900/80 border border-neutral-800 rounded-2xl p-6 backdrop-blur-md lg:col-span-2">
    <h3 className="text-lg font-semibold text-white mb-1">Largest Financial Discrepancies</h3>
    <p className="text-xs text-neutral-400 mb-4">Hover over any bar to inspect full category names and figures.</p>
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={largestDiscrepanciesData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
          <XAxis 
            dataKey="chartKey" 
            stroke="#a3a3a3" 
            fontSize={12} 
            tickFormatter={(value) => {
              const item = largestDiscrepanciesData.find(d => d.chartKey === value);
              if (!item) return "";
              const name = item.fullLocation;
              return name.length > 14 ? name.substring(0, 12) + "..." : name;
            }}
          />
          <YAxis stroke="#a3a3a3" fontSize={12} tickFormatter={(val) => `$${val}`} />
          <Tooltip 
            content={<CustomBarTooltip />} 
            cursor={{ fill: "rgba(255, 255, 255, 0.05)" }}
            isAnimationActive={false}
          />
          <Bar dataKey="Discrepancy" fill="#f59e0b" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
)}
        </div>
      </div>

      {/* Download Action Button */}
      <div className="w-full flex justify-center mt-8 mb-12">
        <button
          onClick={handleDownloadPDF}
          disabled={isExporting}
          className="flex items-center gap-2 text-sm text-neutral-300 hover:text-white bg-neutral-900/80 hover:bg-neutral-800 font-medium px-8 py-3.5 rounded-xl shadow-xl transition-all border border border-neutral-800 backdrop-blur-md cursor-pointer"
        >
          {isExporting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating PDF...
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              Download Charts as PDF
            </>
          )}
        </button>
      </div>
    </WavyBackground>
  );
}