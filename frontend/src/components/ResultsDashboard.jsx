import React from 'react';
import RiskMeter from './RiskMeter';

/**
 * Main results dashboard component
 */
function ResultsDashboard({ result, onNewCheck }) {
    const formatDate = (isoString) => {
        return new Date(isoString).toLocaleString();
    };

    return (
        <div className="w-full max-w-5xl mx-auto space-y-6 animate-fade-in">
            {/* Header */}
            <div className="glass-card p-6">
                <div className="flex items-center justify-between flex-wrap gap-4">
                    <div>
                        <h2 className="text-3xl font-bold gradient-text mb-2">{result.domain}</h2>
                        <p className="text-sm text-gray-400">
                            Analyzed at {formatDate(result.analysis_timestamp)}
                        </p>
                    </div>
                    <button onClick={onNewCheck} className="btn-secondary">
                        <span className="flex items-center">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                            Check Another
                        </span>
                    </button>
                </div>
            </div>

            {/* Risk Score */}
            <div className="glass-card p-8">
                <div className="text-center">
                    <RiskMeter score={result.risk_score} verdict={result.verdict} />
                    <div className="mt-6 grid grid-cols-2 gap-4 max-w-md mx-auto">
                        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                            <p className="text-sm text-gray-400">Confidence</p>
                            <p className="text-2xl font-bold text-blue-400">{Math.round(result.confidence * 100)}%</p>
                        </div>
                        <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                            <p className="text-sm text-gray-400">Risk Level</p>
                            <p className="text-2xl font-bold text-purple-400">{result.risk_score >= 70 ? 'High' : result.risk_score >= 40 ? 'Medium' : 'Low'}</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Detailed Reasons */}
            <div className="glass-card p-6">
                <h3 className="text-xl font-bold mb-4 flex items-center">
                    <svg className="w-6 h-6 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                    </svg>
                    Analysis Report
                </h3>
                <div className="space-y-3">
                    {result.detailed_reasons.map((reason, index) => {
                        const isPositive = reason.includes('✅');
                        const isWarning = reason.includes('⚠️');
                        const isCritical = reason.includes('🚨');

                        let bgClass = 'bg-white/5';
                        let borderClass = 'border-white/10';

                        if (isPositive) {
                            bgClass = 'bg-success-500/10';
                            borderClass = 'border-success-500/30';
                        } else if (isWarning) {
                            bgClass = 'bg-warning-500/10';
                            borderClass = 'border-warning-500/30';
                        } else if (isCritical) {
                            bgClass = 'bg-danger-500/10';
                            borderClass = 'border-danger-500/30';
                        }

                        return (
                            <div
                                key={index}
                                className={`p-4 ${bgClass} border ${borderClass} rounded-lg transition-all duration-300 hover:scale-[1.01]`}
                            >
                                <p className="text-sm leading-relaxed whitespace-pre-line">{reason}</p>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* How We Analyzed This */}
            <div className="glass-card p-6">
                <h3 className="text-xl font-bold mb-4 flex items-center">
                    <svg className="w-6 h-6 mr-2 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    How We Analyzed This Domain
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* WHOIS Analysis */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">📋</span>
                            <h4 className="font-semibold">Domain Registration</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Checked domain age, registrar information, and registration status to identify newly created suspicious domains.
                        </p>
                    </div>

                    {/* SSL Analysis */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">🔒</span>
                            <h4 className="font-semibold">SSL Certificate</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Verified HTTPS security, certificate validity, and encryption strength to ensure secure connections.
                        </p>
                    </div>

                    {/* DNS Analysis */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">🌐</span>
                            <h4 className="font-semibold">DNS Resolution</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Checked IP address resolution and network infrastructure to detect suspicious hosting patterns.
                        </p>
                    </div>

                    {/* Blacklist Check */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">🛡️</span>
                            <h4 className="font-semibold">Security Databases</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Cross-referenced against 8+ blacklist databases including Spamhaus, URIBL, and SORBS for known threats.
                        </p>
                    </div>

                    {/* Hosting Analysis */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">🏢</span>
                            <h4 className="font-semibold">Hosting Provider</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Analyzed hosting service reputation and identified bulletproof hosting indicators commonly used by scammers.
                        </p>
                    </div>

                    {/* Content Analysis */}
                    <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">📄</span>
                            <h4 className="font-semibold">Content Scanning</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Scanned website content for high-risk scam keywords, phishing forms, and suspicious text patterns.
                        </p>
                    </div>

                    {/* AI Analysis */}
                    <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-lg border border-blue-500/30 md:col-span-2">
                        <div className="flex items-center mb-3">
                            <span className="text-2xl mr-3">🤖</span>
                            <h4 className="font-semibold">AI Risk Assessment</h4>
                        </div>
                        <p className="text-sm text-gray-300">
                            Combined machine learning (60%) and rule-based analysis (40%) to generate an explainable risk score with confidence rating.
                        </p>
                    </div>
                </div>

                {/* Privacy Notice */}
                <div className="mt-4 p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                    <p className="text-xs text-center text-purple-300">
                        🔒 Privacy: Technical data is used only for analysis and is not stored or shared
                    </p>
                </div>
            </div>

            {/* Disclaimer */}
            <div className="glass-card p-4 bg-blue-500/10 border-blue-500/30">
                <p className="text-sm text-center text-blue-300">
                    ⚠️ This analysis is automated and should be used as a guide. Always exercise caution when visiting unfamiliar websites.
                </p>
            </div>
        </div>
    );
}

export default ResultsDashboard;
