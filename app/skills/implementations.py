import os
from app.modules.memory_manager import read_memory_file
from app.skills.ticket import (
    create_ticket_skill,
    list_tickets_skill,
    get_ticket_skill,
    done_ticket_skill,
)

 


async def read_full_memory(directory_name: str, file_name: str) -> str:
    """
    Membaca dan mengembalikan seluruh konten dari file memori yang ditentukan.
    """
    try:
        # Menghapus ekstensi .md jika ada, karena fungsi read_memory_file menanganinya
        if file_name.endswith(".md"):
            file_name = file_name[:-3]

        content = await read_memory_file(directory_name, file_name)
        # Mengembalikan string yang jelas untuk LLM agar tahu kontennya
        return f"Berikut adalah konten lengkap dari file '{file_name}':\n\n{content}"
    except FileNotFoundError:
        return f"Error: File '{file_name}' di direktori '{directory_name}' tidak ditemukan."
    except Exception as e:
        return f"Terjadi error yang tidak terduga saat membaca file: {str(e)}"


async def search_memory_by_keyword(directory_name: str, file_name: str, keyword: str) -> str:
    """
    Mencari kata kunci dalam file dan mengembalikan baris yang mengandung kata kunci tersebut.
    """
    try:
        # Menghapus ekstensi .md jika ada
        if file_name.endswith(".md"):
            file_name = file_name[:-3]

        content = await read_memory_file(directory_name, file_name)
        lines = content.splitlines()

        # Mencari baris yang cocok (case-insensitive)
        relevant_lines = [line for line in lines if keyword.lower() in line.lower()]

        if not relevant_lines:
            return f"Keyword '{keyword}' tidak ditemukan dalam file '{file_name}'."

        # Menggabungkan hasil menjadi satu string
        result = "\n".join(relevant_lines)
        return f"Ditemukan hasil untuk keyword '{keyword}' di file '{file_name}':\n\n{result}"
    except FileNotFoundError:
        return f"Error: File '{file_name}' di direktori '{directory_name}' tidak ditemukan."
    except Exception as e:
        return f"Terjadi error yang tidak terduga saat mencari keyword: {str(e)}"

# Daftarkan semua fungsi skill yang tersedia dalam sebuah dictionary.
# Ini memungkinkan kita untuk memanggil fungsi secara dinamis berdasarkan nama.
AVAILABLE_SKILLS = {
    "read_full_memory": read_full_memory,
    "search_memory_by_keyword": search_memory_by_keyword,
    "create_ticket": create_ticket_skill,
    "list_tickets": list_tickets_skill,
    "get_ticket": get_ticket_skill,
    "done_ticket": done_ticket_skill,
}