# Product Principles — NEXUS

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Principles of Being
1. **User Authority & Transparency:** Pengguna memegang kendali penuh atas identitas, memori, dan izin eksekusi. NEXUS transparan mengenai sumber konteks yang digunakannya.
2. **Deterministic Security Over Model Opinion:** Model bahasa (LLM) adalah komponen penalaran, bukan pemutus otorisasi. Keputusan keamanan dan risiko bersifat deterministik.
3. **Store Meaning, Not Everything:** Data chat sementara tidak otomatis menjadi memori permanen. Memori harus dievaluasi nilai pentingnya (*worth storing*), diverifikasi sensitivitasnya, dan dapat dilupakan (*forget semantics*).
4. **Endpoint Agnostic:** Identitas dan kecerdasan berpusat pada NEXUS Core, bukan terikat kaku pada satu UI aplikasi iOS atau satu Mac tertentu.
5. **Fail-Closed by Design:** Jika ada ambiguitas keamanan, izin kadaluarsa, atau kegagalan verifikasi, sistem wajib membatalkan aksi (*fail safe/closed*).
6. **No Phantom Capabilities:** Sistem tidak boleh menjanjikan atau memalsukan kemampuan hardware (misal: menyalakan Mac yang shutdown penuh tanpa dukungan daya/jaringan).
