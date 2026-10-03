# ADR-008: Outbound Persistent WebSocket (WSS) for Mac Agent

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Komputer Mac pengguna umumnya berada di balik NAT rumah/kantor, firewall, atau hotspot seluler tanpa public IP statis.

## Decision
Mac Agent menginisiasi koneksi keluar (**outbound WSS**) ke backend NEXUS. Backend tidak pernah mencoba menghubungi IP lokal Mac secara langsung.
