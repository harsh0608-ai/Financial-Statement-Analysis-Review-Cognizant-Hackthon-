import React, { useState, useRef, useEffect } from 'react';
import { 
  Upload, 
  FileSpreadsheet, 
  Send, 
  Bot, 
  User, 
  HelpCircle, 
  CheckCircle2, 
  ShieldCheck, 
  BarChart3, 
  Sparkles,
  RefreshCw,
  Menu,
  FileCheck,
  Building2,
  FileText
} from 'lucide-react';

// Placeholders for Backend / RAG Services
const uploadFinancialStatement = async (file) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        fileName: file.name,
        fileSize: (file.size / 1024).toFixed(1) + ' KB',
        uploadTime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    }, 1500);
  });
};

const queryRAGChatbot = async (question, fileData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      let response = "I've analyzed the uploaded financial statements. Here are the review findings:";
      
      const q = question.toLowerCase();
      if (q.includes("mathematical accuracy")) {
        response = "Mathematical Accuracy Verification:\n• Balance Sheet totals reconcile across all periods.\n• Operating Expense sub-totals match Income Statement line items perfectly.\n• No rounding discrepancies exceeding $0.01 detected.";
      } else if (q.includes("prior year tie") || q.includes("tie out")) {
        response = "Prior Year Tie-Out Summary:\n• Opening balances match audited FY2024 closing balances.\n• Retained earnings roll-forward reconciles cleanly with net income and distributions.";
      } else if (q.includes("wp-514") || q.includes("wp 514")) {
        response = "WP-514 Analytics Summary:\n• WP-514 schedule has been populated automatically from financial statements.\n• Key financial planning analytics ratios calculated: Debt Service Coverage (1.42x), Current Ratio (2.1x).\n• Ready for working paper review and sign-off.";
      } else if (q.includes("consistency") || q.includes("spelling")) {
        response = "Internal Consistency & Formatting Review:\n• Internal Consistency: Cash flow ending balance matches balance sheet cash reserves.\n• Spelling & Grammar: 0 typographical errors detected across footnotes and schedules.";
      }

      resolve(response);
    }, 1200);
  });
};

const SUGGESTED_QUESTIONS = [
  "What is the mathematical accuracy?",
  "Verify prior year tie out",
  "Check internal consistency & spelling",
  "Generate WP-514 analytics review"
];

export default function FinancialReviewApp() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isBotThinking, setIsBotThinking] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  const chatBottomRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isBotThinking]);

  const handleFileSelect = async (file) => {
    if (!file) return;
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls') && !file.name.endsWith('.csv')) {
      alert('Please upload an Excel sheet or PDF (.xlsx, .xls, .pdf) or CSV file.');
      return;
    }

    setIsUploading(true);
    const result = await uploadFinancialStatement(file);
    setIsUploading(false);
    setUploadedFile(result);

    setMessages([
      {
        sender: 'bot',
        text: `Hello! I have generated, populated, and ingested **${result.fileName}**. You can now review financial statement planning analytics, verify mathematical accuracy, check prior year tie outs, or populate WP-514 schedules.`
      }
    ]);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleSendMessage = async (textToSend) => {
    const query = typeof textToSend === 'string' ? textToSend : inputMessage;
    if (!query.trim() || isBotThinking) return;

    const userMsg = { sender: 'user', text: query };
    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setIsBotThinking(true);

    const botResponseText = await queryRAGChatbot(query, uploadedFile);
    setIsBotThinking(false);
    setMessages((prev) => [...prev, { sender: 'bot', text: botResponseText }]);
  };

  const resetUpload = () => {
    setUploadedFile(null);
    setMessages([]);
  };

  return (
    <div className="w-full min-h-screen m-0 p-0 flex flex-col font-sans bg-gradient-to-br from-slate-50 via-blue-50/50 to-indigo-50/30 text-slate-900">
      
      {/* Top Navigation */}
      <header className="w-full bg-[#0f172a] text-white sticky top-0 z-50 shadow-md">
        <div className="w-full max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={resetUpload}>
            <div className="bg-amber-400 p-2 rounded-lg text-slate-900 font-bold shadow-sm">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-white block leading-none">Banking FinReview</span>
              <span className="text-[10px] text-amber-400 font-mono tracking-wider">STATEMENT ANALYSIS & REVIEW</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-sm font-medium text-amber-400 hover:text-amber-300 transition-colors">Statement Review</a>
            <a href="#" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">About Us</a>
            <a href="#" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">XYZ Page</a>
            
            {uploadedFile && (
              <div className="ml-4 pl-4 border-l border-slate-700 flex items-center space-x-3">
                <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-medium text-slate-300 truncate max-w-[150px]">{uploadedFile.fileName}</span>
                <button 
                  onClick={resetUpload}
                  className="text-slate-400 hover:text-amber-400 transition-colors"
                  title="Upload different file"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            )}
          </nav>

          <div className="md:hidden flex items-center">
            <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-slate-300 hover:text-white p-2">
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden bg-[#1e293b] border-t border-slate-700 px-6 py-4 space-y-4">
            <a href="#" className="block text-sm font-medium text-amber-400">Statement Review</a>
            <a href="#" className="block text-sm font-medium text-slate-300 hover:text-white">About Us</a>
            <a href="#" className="block text-sm font-medium text-slate-300 hover:text-white">XYZ Page</a>
          </div>
        )}
      </header>

      {/* Main Container */}
      <main className="flex-1 w-full flex flex-col justify-center items-center px-4 py-8 sm:px-6 lg:px-8">
        {!uploadedFile ? (
          /* UPLOAD CARD */
          <div className="w-full max-w-3xl bg-white rounded-3xl shadow-[0_10px_40px_rgb(0,0,0,0.05)] border border-slate-200/80 p-8 sm:p-12 my-auto">
            
            <div className="text-center space-y-4 mb-8">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-amber-50 border border-amber-200/80 text-amber-800 text-sm font-semibold">
                <Sparkles className="w-4 h-4 text-amber-600" />
                Banking & Analytics Intelligence
              </div>
              <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-[#0f172a]">
                Financial Statement Analysis & Review
              </h1>
              <p className="text-slate-500 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
                Generate, populate, and review financial statement planning analytics, perform mathematical accuracy checks, prior year tie outs, and prepare WP-514 working papers.
              </p>
            </div>

            {/* Dropzone */}
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-300 ease-out ${
                dragActive 
                  ? 'border-amber-400 bg-amber-50/80 scale-[1.01]' 
                  : 'border-slate-300 bg-slate-50/60 hover:border-[#0f172a] hover:bg-slate-50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".xlsx, .xls, .csv"
                className="hidden"
                onChange={(e) => handleFileSelect(e.target.files[0])}
              />

              {isUploading ? (
                <div className="space-y-4 py-6">
                  <RefreshCw className="w-12 h-12 text-[#0f172a] animate-spin mx-auto" />
                  <div className="text-[#0f172a] font-bold text-lg">Processing financial statements...</div>
                  <div className="text-sm text-slate-500">Populating planning analytics & WP-514 parameters</div>
                </div>
              ) : (
                <div className="space-y-4 py-2">
                  <div className="w-16 h-16 sm:w-20 sm:h-20 bg-white border border-slate-200 shadow-sm rounded-full flex items-center justify-center mx-auto text-[#0f172a]">
                    <Upload className="w-8 h-8 sm:w-10 sm:h-10" />
                  </div>
                  <div>
                    <p className="text-[#0f172a] font-semibold text-lg sm:text-xl">
                      Upload your Financial Statements here
                    </p>
                    <p className="text-sm text-slate-500 mt-1.5 font-medium">
                      or <span className="text-amber-600 underline underline-offset-4 hover:text-amber-700">browse from your computer</span>
                    </p>
                    <p className="text-xs text-slate-400 mt-3">
                      Supports .XLSX, .XLS, .CSV, .PDF (Max 50MB)
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Core Review Capabilities */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 border-t border-slate-100 pt-6">
              <div className="flex flex-col items-center text-center space-y-1.5">
                <div className="bg-[#0f172a] p-2 rounded-lg text-white">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <h4 className="text-xs font-bold text-slate-900">Math Accuracy</h4>
                <p className="text-[11px] text-slate-500">Reconcile cross-totals</p>
              </div>

              <div className="flex flex-col items-center text-center space-y-1.5">
                <div className="bg-[#0f172a] p-2 rounded-lg text-white">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <h4 className="text-xs font-bold text-slate-900">Prior Year Tie Out</h4>
                <p className="text-[11px] text-slate-500">Match opening balances</p>
              </div>

              <div className="flex flex-col items-center text-center space-y-1.5">
                <div className="bg-[#0f172a] p-2 rounded-lg text-white">
                  <FileCheck className="w-4 h-4" />
                </div>
                <h4 className="text-xs font-bold text-slate-900">Consistency & Grammar</h4>
                <p className="text-[11px] text-slate-500">Spelling & logic checks</p>
              </div>

              <div className="flex flex-col items-center text-center space-y-1.5">
                <div className="bg-[#0f172a] p-2 rounded-lg text-white">
                  <FileText className="w-4 h-4" />
                </div>
                <h4 className="text-xs font-bold text-slate-900">WP-514 Analytics</h4>
                <p className="text-[11px] text-slate-500">Auto-populated working papers</p>
              </div>
            </div>
          </div>
        ) : (
          /* CHAT INTERFACE */
          <div className="w-full max-w-4xl flex-1 flex flex-col bg-white border border-slate-200 rounded-3xl shadow-[0_10px_40px_rgb(0,0,0,0.05)] overflow-hidden min-h-[75vh]">
            
            {/* Header */}
            <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
              <div>
                <h2 className="text-lg font-bold text-[#0f172a]">Banking Analysis Assistant</h2>
                <p className="text-xs text-slate-500">Financial statement review and WP-514 audit tool</p>
              </div>
              <div className="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 border border-emerald-200">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Statement Ingested
              </div>
            </div>

            {/* Chat Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/30">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex items-start gap-4 ${
                    msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
                  }`}
                >
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${
                      msg.sender === 'user'
                        ? 'bg-[#0f172a] text-white'
                        : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}
                  >
                    {msg.sender === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                  </div>

                  <div
                    className={`max-w-[85%] sm:max-w-[75%] px-5 py-4 text-sm sm:text-base leading-relaxed whitespace-pre-wrap ${
                      msg.sender === 'user'
                        ? 'bg-[#0f172a] text-white font-medium rounded-2xl rounded-tr-sm shadow-md'
                        : 'bg-white border border-slate-200 text-slate-700 rounded-2xl rounded-tl-sm shadow-sm'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}

              {isBotThinking && (
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-full bg-amber-100 text-amber-800 border border-amber-200 flex items-center justify-center shadow-sm">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div className="bg-white border border-slate-200 text-slate-400 rounded-2xl rounded-tl-sm px-5 py-4 flex items-center space-x-2 shadow-sm">
                    <span className="w-2.5 h-2.5 bg-amber-400 rounded-full animate-bounce"></span>
                    <span className="w-2.5 h-2.5 bg-amber-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                    <span className="w-2.5 h-2.5 bg-amber-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                  </div>
                </div>
              )}
              <div ref={chatBottomRef} />
            </div>

            {/* Input & Suggestions */}
            <div className="p-4 sm:p-6 bg-white border-t border-slate-100 space-y-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-slate-500 flex items-center gap-1 font-semibold mr-2 uppercase tracking-wider">
                  <Sparkles className="w-3.5 h-3.5 text-amber-500" /> Suggestions
                </span>
                {SUGGESTED_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(q)}
                    disabled={isBotThinking}
                    className="text-xs bg-slate-50 hover:bg-amber-50 text-slate-700 hover:text-amber-800 border border-slate-200 hover:border-amber-300 px-3.5 py-2 rounded-full transition-all duration-200 text-left cursor-pointer disabled:opacity-50 font-medium"
                  >
                    {q}
                  </button>
                ))}
              </div>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendMessage();
                }}
                className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-xl p-2 focus-within:border-[#0f172a] focus-within:ring-1 focus-within:ring-[#0f172a] transition-all shadow-inner"
              >
                <input
                  type="text"
                  placeholder="Ask a question about mathematical accuracy, tie out, or WP-514..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  disabled={isBotThinking}
                  className="flex-1 bg-transparent px-4 py-2 text-base text-slate-900 placeholder-slate-400 focus:outline-none disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={!inputMessage.trim() || isBotThinking}
                  className="bg-[#0f172a] hover:bg-slate-800 text-white p-3 rounded-lg font-medium transition-all disabled:opacity-50 disabled:hover:bg-[#0f172a] shadow-sm flex items-center justify-center group"
                >
                  <Send className="w-5 h-5 group-hover:scale-110 transition-transform" />
                </button>
              </form>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}