# ADR-007: Native Swift for macOS Agent

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Mac Agent harus berjalan secara efisien di latar belakang sebagai menu-bar utility, mengakses native macOS APIs secara aman, dan memiliki footprint memori yang sangat kecil.

## Decision
Membangun Mac Agent secara native menggunakan **Swift**.
