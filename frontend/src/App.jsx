import React, { useState } from 'react';
import Header from './components/Header';
import DomainInput from './components/DomainInput';
import LoadingSteps from './components/LoadingSteps';
import ResultsDashboard from './components/ResultsDashboard';
import { checkDomain } from './services/api';
import './index.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCheck = async (domain) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await checkDomain(domain);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze domain. Please try again.');
      console.error('Error checking domain:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewCheck = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen">
      <Header />

      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        {!loading && !result && (
          <>
            <div className="text-center mb-12 max-w-3xl mx-auto">
              <h1 className="text-5xl md:text-6xl font-bold mb-6 gradient-text text-shadow">
                AI-Powered Scam Detection
              </h1>
              <p className="text-xl text-gray-300 leading-relaxed">
                Protect yourself from online scams with our advanced AI analysis.
                We check domains against multiple security databases and use machine learning
                to identify suspicious websites.
              </p>
            </div>

            <DomainInput onCheck={handleCheck} isLoading={loading} />

            {/* Features Section */}
            <section id="features" className="mt-16 scroll-mt-20">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold gradient-text mb-4">Powerful Features</h2>
                <p className="text-gray-300 max-w-2xl mx-auto">
                  Comprehensive security analysis using multiple data sources and AI technology
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-cyan-500 to-teal-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-cyan-500/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Real-Time Analysis</h3>
                  <p className="text-gray-400 text-sm">Instant domain safety checks in 10-30 seconds using parallel processing</p>
                </div>

                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-teal-500/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">AI-Powered Detection</h3>
                  <p className="text-gray-400 text-sm">Machine learning models trained on scam patterns with 60% ML + 40% rule-based scoring</p>
                </div>

                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Explainable Results</h3>
                  <p className="text-gray-400 text-sm">Detailed reports showing exactly why a domain is flagged as safe or suspicious</p>
                </div>

                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-cyan-400/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Multi-Source Checks</h3>
                  <p className="text-gray-400 text-sm">6 analysis services: WHOIS, SSL, DNS, Blacklists (8+ databases), Hosting, Content</p>
                </div>

                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-teal-400 to-cyan-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-teal-400/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Privacy First</h3>
                  <p className="text-gray-400 text-sm">No data storage, No tracking, runs locally - your searches are completely private</p>
                </div>

                <div className="glass-card-hover p-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-cyan-500 via-teal-500 to-blue-600 rounded-lg flex items-center justify-center mb-4 shadow-lg shadow-cyan-500/30">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2">Open Source</h3>
                  <p className="text-gray-400 text-sm">Fully transparent code - no black boxes, verify exactly what the AI is checking</p>
                </div>
              </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works" className="mt-20 scroll-mt-20">
              <div className="text-center mb-12">
                <h2 className="text-4xl font-bold gradient-text mb-4">How It Works</h2>
                <p className="text-gray-300 max-w-2xl mx-auto">
                  Our AI analyzes domains through 6 parallel checks and combines the results for an accurate verdict
                </p>
              </div>

              <div className="max-w-4xl mx-auto space-y-6">
                {/* Step 1 */}
                <div className="glass-card p-6 flex gap-6 items-start">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-cyan-500 to-teal-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-cyan-500/30">
                    1
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2">Data Collection (6 Services)</h3>
                    <p className="text-gray-400 mb-3">
                      When you enter a domain, we simultaneously query 6 different services:
                    </p>
                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-300">
                      <li>📋 <strong>WHOIS:</strong> Domain age & registrar</li>
                      <li>🔒 <strong>SSL:</strong> Certificate validation</li>
                      <li>🌐 <strong>DNS:</strong> IP resolution & infrastructure</li>
                      <li>🛡️ <strong>Blacklists:</strong> 8+ threat databases</li>
                      <li>🏢 <strong>Hosting:</strong> Provider reputation</li>
                      <li>📄 <strong>Content:</strong> NLP keyword analysis</li>
                    </ul>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="glass-card p-6 flex gap-6 items-start">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-teal-500/30">
                    2
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2">Feature Extraction</h3>
                    <p className="text-gray-400">
                      Raw data is converted into 10 machine learning features including domain age, SSL status,
                      blacklist hits, hosting reputation, and content scam scores.
                    </p>
                  </div>
                </div>

                {/* Step 3 */}
                <div className="glass-card p-6 flex gap-6 items-start">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-blue-500/30">
                    3
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2">AI Risk Scoring</h3>
                    <p className="text-gray-400 mb-3">
                      Two analysis methods work together:
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-3 bg-white/5 rounded-lg">
                        <p className="text-sm font-semibold text-blue-400 mb-1">🤖 ML Model (60%)</p>
                        <p className="text-xs text-gray-400">Weighted feature scoring with confidence calculation</p>
                      </div>
                      <div className="p-3 bg-white/5 rounded-lg">
                        <p className="text-sm font-semibold text-purple-400 mb-1">📋 Rules Engine (40%)</p>
                        <p className="text-xs text-gray-400">Pattern matching and heuristic analysis</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Step 4 */}
                <div className="glass-card p-6 flex gap-6 items-start">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-cyan-400/30">
                    4
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2">Final Verdict</h3>
                    <p className="text-gray-400 mb-3">
                      Scores are combined and interpreted:
                    </p>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1 bg-success-500/20 text-success-300 border border-success-500/30 rounded-full text-xs font-semibold">SAFE</span>
                        <span className="text-gray-400">Risk Score 0-39</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1 bg-warning-500/20 text-warning-300 border border-warning-500/30 rounded-full text-xs font-semibold">SUSPICIOUS</span>
                        <span className="text-gray-400">Risk Score 40-69</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1 bg-danger-500/20 text-danger-300 border border-danger-500/30 rounded-full text-xs font-semibold">LIKELY SCAM</span>
                        <span className="text-gray-400">Risk Score 70-100</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Step 5 */}
                <div className="glass-card p-6 flex gap-6 items-start bg-gradient-to-br from-blue-500/10 to-purple-500/10 border-blue-500/30">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-teal-400 to-cyan-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg shadow-teal-400/30">
                    5
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2">Explainable Report</h3>
                    <p className="text-gray-400">
                      Every verdict includes detailed reasons explaining exactly why the domain was flagged,
                      with specific indicators like "Domain is only 15 days old" or "Found 3 high-risk scam keywords."
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}

        {/* Loading State */}
        {loading && <LoadingSteps />}

        {/* Error State */}
        {error && !loading && (
          <div className="max-w-3xl mx-auto">
            <div className="glass-card p-8 border-danger-500/50">
              <div className="text-center">
                <div className="w-16 h-16 bg-danger-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-danger-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-danger-400 mb-2">Analysis Failed</h3>
                <p className="text-gray-300 mb-6">{error}</p>
                <button onClick={handleNewCheck} className="btn-primary">
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <ResultsDashboard result={result} onNewCheck={handleNewCheck} />
        )}

        {/* About Section */}
        {!loading && !result && (
          <section id="about" className="mt-20 scroll-mt-20">
            <div className="max-w-4xl mx-auto">
              <div className="glass-card p-8 md:p-12">
                <div className="text-center mb-8">
                  <h2 className="text-4xl font-bold gradient-text mb-4">About ScamGuard AI</h2>
                  <p className="text-xl text-gray-300">
                    Protecting users from online scams through AI-powered analysis
                  </p>
                </div>

                <div className="space-y-6 text-gray-300">
                  <p className="text-lg leading-relaxed">
                    <strong className="text-white">ScamGuard AI</strong> is a comprehensive domain safety checker that
                    combines multiple security databases, real-time checks, and machine learning to identify
                    potentially dangerous websites before you visit them.
                  </p>

                  <p className="leading-relaxed">
                    In an era where online scams are becoming increasingly sophisticated, we believe everyone
                    deserves access to powerful security tools. That's why ScamGuard AI is <strong className="text-blue-400">completely free</strong>,
                    <strong className="text-purple-400"> open source</strong>, and <strong className="text-green-400">privacy-focused</strong>.
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-8">
                    <div className="p-6 bg-white/5 rounded-lg border border-white/10 text-center">
                      <div className="text-3xl font-bold text-blue-400 mb-2">6+</div>
                      <p className="text-sm text-gray-400">Analysis Services</p>
                    </div>
                    <div className="p-6 bg-white/5 rounded-lg border border-white/10 text-center">
                      <div className="text-3xl font-bold text-purple-400 mb-2">8+</div>
                      <p className="text-sm text-gray-400">Security Databases</p>
                    </div>
                    <div className="p-6 bg-white/5 rounded-lg border border-white/10 text-center">
                      <div className="text-3xl font-bold text-green-400 mb-2">100%</div>
                      <p className="text-sm text-gray-400">Privacy Protected</p>
                    </div>
                  </div>

                  <div className="border-l-4 border-blue-500 pl-6 py-2 bg-blue-500/10 rounded-r-lg">
                    <h3 className="text-lg font-bold text-white mb-2">Our Mission</h3>
                    <p className="text-gray-300">
                      To make the internet safer by providing transparent, explainable AI-powered security
                      analysis that anyone can use and understand. We believe security tools should be
                      accessible, trustworthy, and educational.
                    </p>
                  </div>

                  <h3 className="text-2xl font-bold text-white mt-8 mb-4">Technology Stack</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-4 bg-white/5 rounded-lg text-center">
                      <p className="font-semibold text-white mb-1">FastAPI</p>
                      <p className="text-xs text-gray-400">Backend</p>
                    </div>
                    <div className="p-4 bg-white/5 rounded-lg text-center">
                      <p className="font-semibold text-white mb-1">React</p>
                      <p className="text-xs text-gray-400">Frontend</p>
                    </div>
                    <div className="p-4 bg-white/5 rounded-lg text-center">
                      <p className="font-semibold text-white mb-1">Python ML</p>
                      <p className="text-xs text-gray-400">AI Engine</p>
                    </div>
                    <div className="p-4 bg-white/5 rounded-lg text-center">
                      <p className="font-semibold text-white mb-1">Tailwind CSS</p>
                      <p className="text-xs text-gray-400">Design</p>
                    </div>
                  </div>

                  <div className="border-t border-white/10 pt-6 mt-8 text-center">
                    <p className="text-sm text-gray-400">
                      <strong className="text-white">Open Source</strong> • <strong className="text-white">No Tracking</strong> • <strong className="text-white">No Data Storage</strong>
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      Built with ❤️ for a safer internet
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Footer */}
        <footer className="mt-20 text-center text-gray-500 text-sm">
          <div className="glass-card p-6 max-w-3xl mx-auto">
            <p className="mb-2">
              Built with using FastAPI, React, and AI
            </p>
            <p className="text-xs">
              This tool provides automated analysis and should not be the sole basis for security decisions.
              Always practice safe browsing habits.
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
