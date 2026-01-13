import React from 'react';

/**
 * Circular risk meter component
 */
function RiskMeter({ score, verdict }) {
    const getColor = () => {
        if (score >= 70) return 'danger';
        if (score >= 40) return 'warning';
        return 'success';
    };

    const color = getColor();
    const circumference = 2 * Math.PI * 90;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    const colorClasses = {
        danger: 'text-danger-500',
        warning: 'text-warning-500',
        success: 'text-success-500',
    };

    const strokeColors = {
        danger: '#ef4444',
        warning: '#f59e0b',
        success: '#22c55e',
    };

    return (
        <div className="flex flex-col items-center">
            <div className="relative w-48 h-48">
                <svg className="transform -rotate-90 w-48 h-48">
                    {/* Background circle */}
                    <circle
                        cx="96"
                        cy="96"
                        r="90"
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth="12"
                        fill="none"
                    />
                    {/* Progress circle */}
                    <circle
                        cx="96"
                        cy="96"
                        r="90"
                        stroke={strokeColors[color]}
                        strokeWidth="12"
                        fill="none"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-5xl font-bold ${colorClasses[color]}`}>
                        {Math.round(score)}
                    </span>
                    <span className="text-sm text-gray-400 mt-1">Risk Score</span>
                </div>
            </div>
            <div className="mt-4">
                <span className={`badge badge-${color.toLowerCase()} text-lg px-6 py-2`}>
                    {verdict}
                </span>
            </div>
        </div>
    );
}

export default RiskMeter;
