import React from 'react';

/**
 * Header component with branding and navigation
 */
function Header() {
    return (
        <header className="backdrop-blur-sm bg-white/5 border-b border-white/10 sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 via-teal-500 to-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-cyan-500/50">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold gradient-text text-shadow">ScamGuard AI</h1>
                            <p className="text-xs text-gray-400">AI-Powered Domain Safety Checker</p>
                        </div>
                    </div>

                    <nav className="hidden md:flex items-center space-x-6">
                        <a href="#features" className="text-sm text-gray-300 hover:text-white transition-colors">Features</a>
                        <a href="#how-it-works" className="text-sm text-gray-300 hover:text-white transition-colors">How It Works</a>
                        <a href="#about" className="text-sm text-gray-300 hover:text-white transition-colors">About</a>
                    </nav>

                </div>
            </div>
        </header>
    );
}

export default Header;
