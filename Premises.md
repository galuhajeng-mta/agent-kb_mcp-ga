# Premis
Central Memory adalah solusi untuk masalah fragmentasi pengetahuan AI. Saat ini, prompt, instruksi, dan memori terkait AI tersebar di mana-mana—dalam notebook, dokumen, dan komentar kode. Ini menciptakan inefisiensi dan inkonsistensi.

Bayangkan kesulitan yang dihadapi Wilsen saat melacak iterasi prompt untuk Agent Letta, atau hambatan yang dihadapi Akbar ketika mencoba mengambil konteks yang tepat untuk demo AI document understanding. Terlebih lagi, bisa jadi Alfian dan Ilman menggunakan Code Assistant yang berbeda sehingga menghasilkan output yang tidak konsisten saat mengerjakan proyek yang sama.

Central Memory hadir untuk memecahkan masalah ini dengan menyediakan basis pengetahuan terpusat, memungkinkan iterasi yang terorganisir, pengambilan konteks yang akurat, dan output yang konsisten di seluruh tim dan alat yang digunakan.

---

## Contoh Skenario

### Skenario 1: Iterasi Prompt yang Tidak Efisien

Misalnya, **Wilsen** memiliki tugas untuk membuat **Agent Letta**. Wilsen mencoba melakukan iterasi dengan membuat berbagai versi agent, menggunakan beragam prompt, dan berbagai versi LLM. Tanpa adanya **Central Memory**, Wilsen akan kesulitan melacak prompt mana yang digunakan, versi LLM mana yang paling efektif, atau bagaimana perubahan kecil pada prompt memengaruhi kinerja agent.

**Central Memory** memfasilitasi proses ini dengan memungkinkan Wilsen membuat suatu **koleksi** yang berisi prompt, detail prompt sistem, dan memudahkan untuk recording hasil dari setiap iterasi. Ini memungkinkan Wilsen untuk membandingkan, melacak, dan mengelola semua percobaan dalam satu tempat, sehingga iterasi menjadi lebih cepat dan terorganisir.

### Skenario 2: Mengambil Konteks yang Sulit

**Akbar** perlu melakukan demo cepat tentang pemahaman dokumen berbasis AI (**AI document understanding**), namun alur yang dibuat tidak dapat mengambil **chunk** atau **node graph** yang sesuai. Mencari dan mengidentifikasi konteks yang tepat menjadi hambatan besar.

Dengan **Central Memory**, Akbar dapat dengan mudah mengambil konteks dan menelusuri tautan (**traverse link**) yang sesuai. Hipotesisnya, banyak dokumen di sebuah perusahaan sudah dibuat dalam hierarki terstruktur. **Central Memory** dapat diintegrasikan dengan mudah untuk memanfaatkan struktur ini, memastikan pengambilan konteks yang akurat dan relevan, serta mempercepat proses demo.

### Skenario 3: Inkonsistensi Perilaku dalam Tim

**Alfian** dan **Ilman** bekerja pada repositori yang sama, namun mereka menggunakan dua **Code Assistant** yang berbeda, yang tentu saja menghasilkan perilaku yang berbeda. Ini dapat menyebabkan inkonsistensi dalam output kode dan membuang waktu untuk menyelaraskan hasil.

Dengan memanfaatkan **Central Memory - Instruct Horizon**, kedua code assistant dapat diberikan **konteks yang tepat** yang sama. Dengan begitu, mereka dapat menghasilkan output yang selaras, konsisten, dan **reproducible**, tidak peduli code assistant mana yang digunakan. Ini memastikan kolaborasi yang lebih mulus dan mengurangi kesalahan yang disebabkan oleh perbedaan perilaku alat.

---

## Fleksibilitas Akses dan Kontrol Penuh

**Central Memory** dirancang untuk dapat diakses melalui berbagai alur, memberikan fleksibilitas tinggi untuk iterasi dan verifikasi:

- **Akses Langsung via Host Volume**: Memory dapat diakses langsung melalui host volume, memungkinkan integrasi yang mudah dan cepat dengan sistem lokal.
- **FastAPI Endpoint**: Endpoint API menyediakan cara yang modern dan efisien untuk berinteraksi dengan memory secara terprogram.
- **MCP Endpoint**: Endpoint khusus untuk interaksi dengan **MCP** membuat integrasi dengan AI bisa dilakukan dengan sangat mudah.
- **Obsidian Web-App**: Antarmuka visual melalui aplikasi web Obsidian memudahkan pengguna untuk melihat, mengedit, dan memverifikasi memory secara intuitif.

Berbagai cara akses ini memastikan bahwa **iterasi** dan **verifikasi** terhadap memori yang digunakan dapat dilakukan dengan sangat mudah dan efisien.

Selain itu, dimungkinkan pula bahwa **Central Memory** ini dibuat menjadi **open-source**. Jika suatu perusahaan membutuhkan **manajemen knowledge base** mereka sendiri secara mandiri, mereka dapat dengan mudah melakukan **on-premise deployment**, memberikan kontrol penuh dan keamanan data tanpa harus bergantung pada pihak ketiga.

---

## Membuka Jalan untuk Masa Depan

### Otonomi Pengguna Akhir

**Prompt** hanyalah langkah pertama dari sebuah **AI Agent**. Ke depannya, sangat penting untuk memberdayakan pengguna akhir (end-user) untuk mengelola prompt mereka sendiri secara mandiri. **Central Memory** menyediakan fondasi yang kuat untuk otonomi ini.

### Pengetahuan yang Selalu Dinamis

**Knowledge graph** suatu perusahaan tidak pernah statis, ia selalu berevolusi. Jauh lebih efektif jika ada sistem di mana pengguna dapat dengan mudah melakukan **ingestion OCR** dan **mengedit pengetahuan** secara mandiri. **Central Memory** membuat proses ini menjadi kenyataan.

### Fokus pada Nilai Utama

Sebagai sebuah perusahaan AI, kita harus melangkah lebih jauh dari sekadar manajemen prompt. Banyak pekerjaan penting yang menanti: **finetuning**, **engineering decision**, **evaluasi**, **skalabilitas**, maupun **reliabilitas**. Dengan adanya **Central Memory**, kita dapat membebaskan waktu dan sumber daya untuk mengejar keunggulan-keunggulan tersebut, sehingga fokus bisa beralih dari sekadar mengorganisir 'prompt' maupun juggling dengan 'knowledge' menjadi membangun produk AI yang benar-benar unggul.