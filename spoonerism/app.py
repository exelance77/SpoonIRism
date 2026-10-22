import streamlit as st
import random
import re

# Sayfa Yapılandırması
st.set_page_config(page_title="Spoonerism Ultimate Challenge", page_icon="🏆", layout="centered")

# Oturum Durumu (Session State) Başlatma
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "last_result" not in st.session_state:
    st.session_state.last_result = ""

CATEGORY_1_BASICS = [
    ("Relational Internations", "International Relations", "Uluslararası İlişkiler (Akademik Disiplin)"),
    ("Poreign Folicy", "Foreign Policy", "Dış Politika"),
    ("Polinational Intertics", "International Politics", "Uluslararası Siyaset"),
    ("Porld Wolitics", "World Politics", "Dünya Siyaseti"),
    ("Miplodacy", "Diplomacy", "Diplomasi"),
    ("Lipdomat", "Diplomat", "Diplomat"),
    ("Bemassy", "Embassy", "Büyükelçilik"),
    ("Affeign Forairs", "Foreign Affairs", "Dış İşleri"),
    ("Intional Naterest", "National Interest", "Ulusal Çıkar"),
    ("Sational Necurity", "National Security", "Ulusal Güvenlik"),
    ("Roveseignty", "Sovereignty", "Egemenlik"),
    ("Station Nate", "Nation State", "Ulus Devlet"),
    ("Scitical Polience", "Political Science", "Siyaset Bilimi"),
    ("Powitical Poler", "Political Power", "Siyasi Güç / İktidar"),
    ("Polic Publicy", "Public Policy", "Kamu Politikası")
]

CATEGORY_2_ORGS = [
    ("Natited Unions", "United Nations", "Birleşmiş Milletler (BM)"),
    ("Stated Unites", "United States", "Amerika Birleşik Devletleri (ABD)"),
    ("Upean Euronion", "European Union", "Avrupa Birliği (AB)"),
    ("Ana Tolliance", "NATO Alliance", "Kuzey Atlantik Antlaşması Örgütü"),
    ("Cecurity Souncil", "Security Council", "Güvenlik Konseyi"),
    ("Aseneral Gsembly", "General Assembly", "Genel Kurul"),
    ("Borld Wank", "World Bank", "Dünya Bankası"),
    ("Orld Wrade Torganization", "World Trade Organization", "Dünya Ticaret Örgütü (DTÖ)"),
    ("Compean Euromission", "European Commission", "Avrupa Komisyonu"),
    ("Parpean Euroliament", "European Parliament", "Avrupa Parlamentosu"),
    ("Wold Car", "Cold War", "Soğuk Savaş"),
    ("Wivil Car", "Civil War", "İç Savaş"),
    ("Waxy Pror", "Proxy War", "Vekalet Savaşı"),
    ("Treace Peaty", "Peace Treaty", "Barış Antlaşması"),
    ("Ronflict Cesolution", "Conflict Resolution", "Çatışma Çözümü")
]

CATEGORY_3_THEORY = [
    ("Lawnational Inter", "International Law", "Uluslararası Hukuk"),
    ("Ruman Hights", "Human Rights", "İnsan Hakları"),
    ("Tree Frade", "Free Trade", "Serbest Ticaret"),
    ("Ecobal Glonomy", "Global Economy", "Küresel Ekonomi"),
    ("Devolomic Econopment", "Economic Development", "Ekonomik Kalkınma"),
    ("Brade Talance", "Trade Balance", "Ticaret Dengesi"),
    ("Zlobaligation", "Globalization", "Küreselleşme"),
    ("Relitical Poalism", "Political Realism", "Siyasi Realizm (Gerçekçilik)"),
    ("Lilitical Poberalism", "Political Liberalism", "Siyasi Liberalizm"),
    ("Pemocratic Deace", "Democratic Peace", "Demokratik Barış Teorisi"),
    ("Tanionalism", "Nationalism", "Milliyetçilik"),
    ("Tapicalism", "Capitalism", "Kapitalizm"),
    ("Momcunism", "Communism", "Komünizm"),
    ("Helf Selp", "Self Help", "Kendi Kendine Yetebilme"),
    ("Nersona Gon Prata", "Persona non grata", "İstenmeyen Adam")
]

CATEGORY_4_LEADERS = [
    ("Porld Weace", "World Peace", "Dünya Barışı"),
    ("Mustafa Kemal Atatürk", "Mustafa Kemal Atatürk", "❤️(1881-193∞)🤍"),
    ("Bapoleon Nonaparte", "Napoleon Bonaparte", "Fransız İmparatoru (1769–1821)"),
    ("Hadolf Itler", "Adolf Hitler", "Nazi Almanyası Lideri (1889–1945)"),
    ("Miccolo Nachiavelli", "Niccolo Machiavelli", "İtalyan Siyaset Filozofu (1469–1527)"),
    ("Powt Sofer", "Soft Power", "Yumuşak Güç"),
    ("Pard Hower", "Hard Power", "Sert Güç")
]

BITMOJIS = ["😎", "🚀", "🦊", "🦁", "🤖", "👻", "🦄", "🔥", "⚡", "👑", "🎯", "🐱", "🐼", "💀", "👽", "🤠", "🏆", "🌟", "🍀", "💎"]

def normalize_text(text):
    return re.sub(r'[\s\-]', '', text.lower())

# --- GİRİŞ EKRANI ---
if not st.session_state.game_started:
    st.title("🏆 Spoonerism Ultimate Challenge")
    st.markdown("Uluslararası İlişkiler ve Liderler Kelime Bulmaca Oyunu")
    
    with st.form("login_form"):
        player_name = st.text_input("Oyuncu Adınızı Girin:", max_chars=20)
        player_bitmoji = st.selectbox("Bir Bitmoji Seçin:", BITMOJIS)
        submitted = st.form_submit_button("OYUNA BAŞLA")
        
        if submitted:
            if not player_name.strip():
                st.warning("Lütfen geçerli bir oyuncu adı girin!")
            else:
                st.session_state.player_name = player_name.strip()
                st.session_state.player_bitmoji = player_bitmoji
                
                pool_1 = random.sample(CATEGORY_1_BASICS, min(5, len(CATEGORY_1_BASICS)))
                pool_2 = random.sample(CATEGORY_2_ORGS, min(5, len(CATEGORY_2_ORGS)))
                pool_3 = random.sample(CATEGORY_3_THEORY, min(5, len(CATEGORY_3_THEORY)))
                pool_4 = random.sample(CATEGORY_4_LEADERS, min(5, len(CATEGORY_4_LEADERS)))
                
                combined = pool_1 + pool_2 + pool_3 + pool_4
                random.shuffle(combined)
                st.session_state.questions = combined[:20]
                
                st.session_state.current_idx = 0
                st.session_state.correct_count = 0
                st.session_state.show_feedback = False
                st.session_state.game_started = True
                st.rerun()

# --- OYUN EKRANI ---
else:
    if st.session_state.current_idx < len(st.session_state.questions):
        st.subheader(f"Oyuncu: {st.session_state.player_bitmoji} {st.session_state.player_name}")
        st.write(f"Soru: {st.session_state.current_idx + 1} / 20 | Doğru Sayısı: {st.session_state.correct_count}")
        st.progress((st.session_state.current_idx + 1) / 20)
        
        clue, correct_ans, description = st.session_state.questions[st.session_state.current_idx]
        
        st.markdown(f"### İpucu (Spoonerism):")
        st.info(f"👉 **{clue}** 👈")
        
        # Eğer henüz cevap verilmediyse giriş kutusunu göster
        if not st.session_state.show_feedback:
            with st.form(f"q_form_{st.session_state.current_idx}"):
                user_input = st.text_input("Doğrusu nedir?", key=f"input_{st.session_state.current_idx}")
                answer_submitted = st.form_submit_button("Cevapla")
                
                if answer_submitted:
                    if user_input.strip():
                        if normalize_text(user_input) == normalize_text(correct_ans):
                            st.session_state.correct_count += 1
                            st.session_state.last_result = ("success", f"✓ DOĞRU! ({correct_ans})")
                        else:
                            st.session_state.last_result = ("error", f"✗ YANLIŞ! Doğrusu: {correct_ans}")
                        
                        st.session_state.last_desc = description
                        st.session_state.show_feedback = True
                        st.rerun()
                    else:
                        st.warning("Lütfen bir cevap yazın!")
        else:
            # Cevap verildiğinde sonucu göster ve tek tıkla sonraki soruya geç
            res_type, res_text = st.session_state.last_result
            if res_type == "success":
                st.success(res_text)
            else:
                st.error(res_text)
            
            st.markdown(f"📖 *Açıklama: {st.session_state.last_desc}*")
            
            if st.button("Sonraki Soruya Geç ➔"):
                st.session_state.show_feedback = False
                st.session_state.current_idx += 1
                st.rerun()
    
    # --- SONUÇ VE LİDERLİK TABLOSU ---
    else:
        st.balloons()
        st.title("🏆 OYUN BİTTİ - LİDERLİK TABLOSU 🏆")
        
        total_score = st.session_state.correct_count * 50
        
        player_result = {
            "name": st.session_state.player_name,
            "bitmoji": st.session_state.player_bitmoji,
            "score": total_score,
            "correct": st.session_state.correct_count
        }
        
        if not st.session_state.leaderboard or st.session_state.leaderboard[-1] != player_result:
            st.session_state.leaderboard.append(player_result)
            st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
        
        st.metric(label="Toplam Puanınız", value=f"{total_score} Puan", delta=f"{st.session_state.correct_count}/20 Doğru")
        
        st.markdown("### 🌟 En İyi Skorlar")
        for i, entry in enumerate(st.session_state.leaderboard[:10]):
            rank = i + 1
            if rank == 1:
                st.markdown(f"👑 **1. [ALTIN] {entry['bitmoji']} {entry['name']} — {entry['score']} Puan** ({entry['correct']}/20 Doğru)")
            elif rank == 2:
                st.markdown(f"🥈 **2. [GÜMÜŞ] {entry['bitmoji']} {entry['name']} — {entry['score']} Puan** ({entry['correct']}/20 Doğru)")
            elif rank == 3:
                st.markdown(f"🥉 **3. [BRONZ] {entry['bitmoji']} {entry['name']} — {entry['score']} Puan** ({entry['correct']}/20 Doğru)")
            else:
                st.markdown(f"   {rank}. {entry['bitmoji']} {entry['name']} — {entry['score']} Puan ({entry['correct']}/20 Doğru)")
        
        if st.button("YENİ OYUNCU İLE BAŞLA"):
            st.session_state.game_started = False
            st.session_state.show_feedback = False
            st.rerun()