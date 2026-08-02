import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("React Error Caught:", error, errorInfo);
  }

  handleReset = () => {
    // Clear any local storage that might cause crash loop
    localStorage.clear();
    // Navigate back to root and reload
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'Vazirmatn, sans-serif' }} dir="rtl">
          <h2 style={{ color: '#E74C3C' }}>متاسفانه خطایی در نمایش این صفحه رخ داد!</h2>
          <p style={{ color: '#555' }}>
            برای حل مشکل روی دکمه زیر کلیک کنید تا برنامه بازنشانی شود.
          </p>
          <button
            onClick={this.handleReset}
            style={{
              padding: '10px 20px',
              background: '#3498DB',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              marginTop: '15px',
              fontWeight: 'bold'
            }}>
            بازگشت به صفحه اصلی
          </button>

          <div style={{ marginTop: '30px', padding: '15px', background: '#f8d7da', color: '#721c24', borderRadius: '5px', textAlign: 'left', direction: 'ltr', fontSize: '12px', overflowX: 'auto' }}>
            <code>{this.state.error && this.state.error.toString()}</code>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
