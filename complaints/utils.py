"""
Smart Garbage Complaint System — Email Utilities

This module handles sending email notifications to municipal authorities
when new complaints are submitted. It sends a formatted HTML email with
all complaint details.

Configuration:
    Email settings are configured in settings.py.
    By default, emails are printed to the console (for development).
    To send real emails via Gmail SMTP, update your .env file.

Future Integration:
    This module can be extended to:
    - Send SMS notifications via Twilio
    - Push to Swachh Bharat Mission API
    - Integrate with WhatsApp Business API
    - Send automated status update emails to complainants
"""

import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_complaint_notification(complaint):
    """
    Send an email notification about a new complaint to the municipal authority.

    Args:
        complaint: A Complaint model instance

    Returns:
        bool: True if email was sent successfully, False otherwise

    The email includes:
        - Complaint reference number
        - Reporter details
        - Location information
        - Description and priority
        - Link to Google Maps (if provided)
    """
    subject = f"🗑️ New Garbage Complaint [{complaint.reference_number}] — {complaint.location_text[:50]}"

    # Build HTML email body
    html_message = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: #00d4aa; margin: 0; font-size: 24px;">🗑️ Smart Garbage Complaint System</h1>
            <p style="color: #a0aec0; margin-top: 8px;">New Complaint Received</p>
        </div>

        <div style="background: #ffffff; padding: 30px; border: 1px solid #e2e8f0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; color: #4a5568; width: 35%;">
                        Reference No.
                    </td>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; color: #2d3748;">
                        <strong style="color: #00d4aa;">{complaint.reference_number}</strong>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; color: #4a5568;">
                        Reporter
                    </td>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; color: #2d3748;">
                        {complaint.reporter_name}<br>
                        <small style="color: #718096;">{complaint.reporter_email}</small>
                        {f'<br><small style="color: #718096;">📞 {complaint.reporter_phone}</small>' if complaint.reporter_phone else ''}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; color: #4a5568;">
                        📍 Location
                    </td>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; color: #2d3748;">
                        {complaint.location_text}
                        {f'<br><a href="{complaint.google_maps_link}" style="color: #3182ce;">View on Google Maps →</a>' if complaint.google_maps_link else ''}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; color: #4a5568;">
                        ⚡ Priority
                    </td>
                    <td style="padding: 12px; border-bottom: 1px solid #eee; color: #2d3748;">
                        <span style="background: {'#fed7d7' if complaint.priority in ['high', 'critical'] else '#fefcbf'}; padding: 4px 12px; border-radius: 4px; font-weight: bold;">
                            {complaint.get_priority_display()}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; font-weight: bold; color: #4a5568;" colspan="2">
                        📝 Description
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; color: #4a5568; line-height: 1.6;" colspan="2">
                        {complaint.description}
                    </td>
                </tr>
            </table>
        </div>

        <div style="background: #1a1a2e; padding: 20px; text-align: center; border-radius: 0 0 8px 8px;">
            <p style="color: #a0aec0; margin: 0; font-size: 12px;">
                Smart Garbage Complaint System — Powered by Django<br>
                This is an automated notification. Please review and take action.
            </p>
        </div>
    </body>
    </html>
    """

    # Plain text fallback for email clients that don't support HTML
    plain_message = f"""
NEW GARBAGE COMPLAINT — {complaint.reference_number}
{'='*50}

Reporter: {complaint.reporter_name} ({complaint.reporter_email})
Phone: {complaint.reporter_phone or 'Not provided'}
Location: {complaint.location_text}
Google Maps: {complaint.google_maps_link or 'Not provided'}
Priority: {complaint.get_priority_display()}

Description:
{complaint.description}

{'='*50}
Smart Garbage Complaint System — Automated Notification
    """

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.MUNICIPAL_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Email notification sent for complaint {complaint.reference_number}")
        return True

    except Exception as e:
        # Log the error but don't crash the application
        logger.error(f"❌ Failed to send email for {complaint.reference_number}: {e}")
        return False


def send_status_update_email(complaint):
    """
    Send a status update email to the complainant when their complaint
    status changes. This keeps citizens informed about progress.

    Args:
        complaint: A Complaint model instance with updated status
    """
    subject = f"Update on Your Complaint [{complaint.reference_number}]"

    status_messages = {
        'pending': 'Your complaint has been received and is awaiting review.',
        'in_progress': 'Great news! Your complaint is now being addressed by our team.',
        'resolved': '✅ Your complaint has been resolved. Thank you for keeping our city clean!',
    }

    message = f"""
Dear {complaint.reporter_name},

{status_messages.get(complaint.status, 'Your complaint status has been updated.')}

Complaint Reference: {complaint.reference_number}
Location: {complaint.location_text}
Current Status: {complaint.get_status_display()}

{f'Admin Remarks: {complaint.admin_remarks}' if complaint.admin_remarks else ''}

Thank you for helping us maintain a cleaner environment!

— Smart Garbage Complaint System
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[complaint.reporter_email],
            fail_silently=False,
        )
        logger.info(f"✅ Status update email sent to {complaint.reporter_email}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send status update: {e}")
        return False
