"""
Smart Garbage Complaint System — Complaint Model

This module defines the Complaint model which stores all garbage complaint
data submitted by citizens. Each complaint includes:
- Reporter information (name, email, phone)
- Location details (text description + optional Google Maps link)
- Complaint description and photographic evidence
- Status tracking (Pending → In Progress → Resolved)
- Timestamps for auditing

Future Integration:
    This model is designed to be compatible with government systems like
    Swachh Bharat Mission. Fields like `location_text` and `status` can
    be mapped to SBM API endpoints for automated complaint forwarding.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid


class Complaint(models.Model):
    """
    Represents a single garbage complaint filed by a citizen.

    The complaint lifecycle:
        1. Citizen submits complaint → status = 'pending'
        2. Municipal authority reviews → status = 'in_progress'
        3. Issue resolved → status = 'resolved'
    """

    # ─── Status Choices ───────────────────────────────────────────────────
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    # ─── Complaint Priority Levels ────────────────────────────────────────
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # ─── Unique Reference Number ──────────────────────────────────────────
    # Auto-generated reference number for easy tracking (e.g., GC-a1b2c3d4)
    reference_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated unique reference number for this complaint"
    )

    # ─── Reporter Information ─────────────────────────────────────────────
    # User FK is optional — anonymous complaints are allowed
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='complaints',
        help_text="Linked user account (optional — anonymous submissions allowed)"
    )
    reporter_name = models.CharField(
        max_length=100,
        help_text="Full name of the person reporting the issue"
    )
    reporter_email = models.EmailField(
        help_text="Email address for complaint status updates"
    )
    reporter_phone = models.CharField(
        max_length=15,
        blank=True,
        help_text="Contact phone number (optional)"
    )

    # ─── Location Details ─────────────────────────────────────────────────
    location_text = models.CharField(
        max_length=300,
        help_text="Describe the location (e.g., 'Near Sector 5 Market, Noida')"
    )
    google_maps_link = models.URLField(
        blank=True,
        help_text="Paste Google Maps link for precise location (optional)"
    )

    # ─── Complaint Details ────────────────────────────────────────────────
    description = models.TextField(
        help_text="Detailed description of the garbage issue"
    )
    image = models.ImageField(
        upload_to='complaints/%Y/%m/',
        help_text="Upload a photo of the garbage issue for evidence"
    )

    # ─── Status and Priority ─────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the complaint"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Priority level of the complaint"
    )

    # ─── Admin Notes ──────────────────────────────────────────────────────
    admin_remarks = models.TextField(
        blank=True,
        help_text="Internal remarks by municipal authority staff"
    )

    # ─── Timestamps ──────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest complaints first
        verbose_name = 'Garbage Complaint'
        verbose_name_plural = 'Garbage Complaints'

    def save(self, *args, **kwargs):
        """Generate a unique reference number on first save."""
        if not self.reference_number:
            self.reference_number = f"GC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.reference_number}] {self.location_text[:50]} — {self.get_status_display()}"

    @property
    def status_color(self):
        """Return a Bootstrap color class based on complaint status."""
        colors = {
            'pending': 'warning',
            'in_progress': 'info',
            'resolved': 'success',
        }
        return colors.get(self.status, 'secondary')

    @property
    def priority_color(self):
        """Return a Bootstrap color class based on priority."""
        colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'dark',
        }
        return colors.get(self.priority, 'secondary')
