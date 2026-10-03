/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    let rawTarget = (process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000').trim().replace(/\/+$/, '').replace(/\/api$/, '');
    if (rawTarget && !rawTarget.startsWith('http://') && !rawTarget.startsWith('https://')) {
      rawTarget = `https://${rawTarget}`;
    }
    return [
      {
        source: '/api/:path*',
        destination: `${rawTarget}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;