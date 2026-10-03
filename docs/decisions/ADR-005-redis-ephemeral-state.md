# ADR-005: Redis for Ephemeral State, Presence, and Caching

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Sistem membutuhkan penyimpanan data sementara yang sangat cepat untuk pelacakan detak jantung (*heartbeat*) Mac Agent, rate limiting, pub/sub realtime, dan caching jangka pendek.

## Decision
Menggunakan **Redis** semata-mata untuk state efemeral (*short-lived state*). Redis **BUKAN** sumber kebenaran jangka panjang.
