import React, { useState } from 'react';

/**
 * Domain input form component
 */
function DomainInput({ onCheck, isLoading }) {
    const [domain, setDomain] = useState('');
    const [error, setError] = useState('');

    const validateDomain = (value) => {
        // Basic domain validation
        const domainPattern = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$/i;
        return domainPattern.test(value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        const cleanDomain = domain.trim().toLowerCase()
            .replace(/^https?:\/\//, '')
            .replace(/^www\./, '')
            .split('/')[0];

        if (!cleanDomain) {
            setError('Please enter a domain name');
            return;
        }

        if (!validateDomain(cleanDomain)) {
            setError('Please enter a valid domain (e.g., example.com)');
            return;
        }

        onCheck(cleanDomain);
    };

    const handleExampleClick = (exampleDomain) => {
        setDomain(exampleDomain);
        setError('');
    };

    return (
        <div className="w-full max-w-3xl mx-auto">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="glass-card p-8">
                    <div className="mb-6 text-center">
                        <h2 className="text-3xl font-bold mb-2 gradient-text">Check Website Safety</h2>
                        <p className="text-gray-300">Enter a domain to analyze for potential scam indicators</p>
                    </div>

                    <div className="relative">
                        <input
                            type="text"
                            value={domain}
                            onChange={(e) => {
                                setDomain(e.target.value);
                                setError('');
                            }}
                            placeholder="example.com"
                            className="input-field text-lg"
                            disabled={isLoading}
                            autoFocus
                        />
                        <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                    </div>

                    {error && (
                        <div className="mt-3 p-3 bg-danger-500/20 border border-danger-500/30 rounded-lg text-danger-300 text-sm">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="btn-primary w-full mt-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Analyzing...
                            </span>
                        ) : (
                            <span className="flex items-center justify-center">
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                </svg>
                                Check Domain
                            </span>
                        )}
                    </button>

                    <div className="mt-6">
                        <p className="w-full text-center text-sm text-gray-400 mb-3">Try examples:</p>

                        {/* Safe & Popular Websites */}
                        <div className="mb-3">
                            <p className="text-xs text-gray-500 text-center mb-2">✅ Safe & Popular</p>
                            <div className="flex flex-wrap gap-2 justify-center">
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('google.com')}
                                    className="px-3 py-1 text-xs bg-success-500/10 hover:bg-success-500/20 border border-success-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    google.com
                                </button>

                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('amazon.com')}
                                    className="px-3 py-1 text-xs bg-success-500/10 hover:bg-success-500/20 border border-success-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    amazon.com
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('wikipedia.org')}
                                    className="px-3 py-1 text-xs bg-success-500/10 hover:bg-success-500/20 border border-success-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    wikipedia.org
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('microsoft.com')}
                                    className="px-3 py-1 text-xs bg-success-500/10 hover:bg-success-500/20 border border-success-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    microsoft.com
                                </button>
                            </div>
                        </div>

                        {/* Suspicious Patterns */}
                        <div>
                            <p className="text-xs text-gray-500 text-center mb-2">⚠️ Test Suspicious Patterns</p>
                            <div className="flex flex-wrap gap-2 justify-center">
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('verify-account-now.xyz')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    verify-account-now.xyz
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('free-crypto-giveaway.club')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    free-crypto-giveaway.club
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('urgent-update-required.top')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    urgent-update-required.top
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('payment-suspended.online')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    payment-suspended.online
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('claim-prize-winner.site')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    claim-prize-winner.site
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('bitcoin-doubler-2024.tk')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    bitcoin-doubler-2024.tk
                                </button>
                                <button
                                    type="button"
                                    onClick={() => handleExampleClick('security-alert-action.ml')}
                                    className="px-3 py-1 text-xs bg-warning-500/10 hover:bg-warning-500/20 border border-warning-500/30 rounded-full transition-all"
                                    disabled={isLoading}
                                >
                                    security-alert-action.ml
                                </button>
                            </div>
                        </div>

                        <p className="text-xs text-gray-500 text-center mt-3 italic">
                            💡 Tip: Test patterns help you understand how the AI detects scams
                        </p>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default DomainInput;
