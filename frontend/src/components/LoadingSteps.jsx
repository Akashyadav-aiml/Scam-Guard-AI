import React from 'react';

/**
 * Loading component with animated progress steps
 */
function LoadingSteps() {
    const steps = [
        { id: 1, name: 'WHOIS Lookup', icon: '🔍' },
        { id: 2, name: 'SSL Verification', icon: '🔒' },
        { id: 3, name: 'DNS Resolution', icon: '🌐' },
        { id: 4, name: 'Blacklist Check', icon: '🛡️' },
        { id: 5, name: 'Content Analysis', icon: '📄' },
        { id: 6, name: 'AI Evaluation', icon: '🤖' },
    ];

    return (
        <div className="w-full max-w-3xl mx-auto">
            <div className="glass-card p-8">
                <div className="text-center mb-8">
                    <div className="inline-block">
                        <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
                    </div>
                    <h3 className="text-2xl font-bold mt-4 gradient-text">Analyzing Domain</h3>
                    <p className="text-gray-400 mt-2">Running comprehensive security checks...</p>
                </div>

                <div className="space-y-3">
                    {steps.map((step, index) => (
                        <div
                            key={step.id}
                            className="flex items-center space-x-4 p-4 bg-white/5 rounded-lg border border-white/10 animate-pulse"
                            style={{
                                animationDelay: `${index * 0.1}s`,
                            }}
                        >
                            <div className="text-2xl">{step.icon}</div>
                            <div className="flex-1">
                                <p className="font-medium text-white">{step.name}</p>
                                <div className="mt-2 h-1 bg-white/10 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full shimmer w-full"></div>
                                </div>
                            </div>
                            <div className="text-blue-400">
                                <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                    <p className="text-sm text-center text-blue-300">
                        ℹ️ This process may take 10-30 seconds to complete all checks
                    </p>
                </div>
            </div>
        </div>
    );
}

export default LoadingSteps;
