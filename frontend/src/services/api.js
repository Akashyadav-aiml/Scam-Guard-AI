/**
 * API Service for communicating with the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Check domain safety
 * @param {string} domain - Domain to check
 * @returns {Promise<Object>} - Analysis results
 */
export async function checkDomain(domain) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/check-domain?domain=${encodeURIComponent(domain)}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Check API health
 * @returns {Promise<Object>} - Health status
 */
export async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`Health check failed: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Health Check Error:', error);
        throw error;
    }
}
