# Privacy & Security Notice

## Data Handling

### What We Analyze
ScamGuard AI analyzes domains using the following methods:
- **Domain Registration**: WHOIS lookups for age and registrar information
- **SSL Certificates**: Certificate validation and security checks
- **DNS Resolution**: IP address and network infrastructure verification
- **Security Databases**: Cross-reference with public blacklist databases
- **Hosting Provider**: Reputation analysis of hosting services
- **Content Scanning**: Keyword detection and pattern matching
- **AI Risk Assessment**: Machine learning-based threat prediction

### Privacy Commitment

**✅ No Data Storage**: Analysis results are NOT stored on our servers

**✅ No Tracking**: We do not track, log, or save domains you analyze

**✅ No Sharing**: Your searches are private and never shared with third parties

**✅ Client-Side Display**: All analysis happens server-side temporarily and results are displayed directly to you

**✅ No Personal Data**: We do not collect, store, or request any personal information

### Technical Details Display

The application now shows a user-friendly **"How We Analyzed This Domain"** section instead of raw technical signals. This provides:
- Clear explanations of analysis methods
- No exposure of sensitive technical data
- Educational information about cybersecurity practices
- Privacy-conscious design

### Local Installation

For maximum privacy, you can run ScamGuard AI entirely on your local machine:
```bash
# Both servers run locally - no external data transmission
Backend: http://localhost:8000
Frontend: http://localhost:5173
```

### Data Transmission

When you analyze a domain:
1. Your browser sends the domain name to the local API server
2. The server performs analysis (WHOIS, SSL, DNS, etc.)
3. Results are sent back to your browser
4. **Nothing is stored permanently**

### Open Source

All code is available for review - you can verify exactly what the application does with your data.

---

**Last Updated**: 2026-01-14  
**Version**: 1.0.0
