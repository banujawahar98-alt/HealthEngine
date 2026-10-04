import React from 'react';
import { AlertCircle } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  return (
    <div className="disclaimer-banner">
      <AlertCircle size={16} />
      <span>
        <strong>Notice:</strong> This application provides screening and well-being support only. It does not diagnose mental-health conditions and does not replace professional medical care.
      </span>
    </div>
  );
};
