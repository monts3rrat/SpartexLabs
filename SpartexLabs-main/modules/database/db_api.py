import sqlite3
import re


def get_connection():
    return sqlite3.connect("./modules/database/SQLdatabase.db")


class ReferalSystem:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT 1 FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            return result is not None

    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id:
                self.cursor.execute(
                    "INSERT INTO users (user_id, referrer_id) VALUES (?, ?)",
                    (user_id, referrer_id),
                )
            else:
                self.cursor.execute(
                    "INSERT INTO users (user_id) VALUES (?)", (user_id,)
                )
            self.connection.commit()

    def count_referals(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT COUNT(id) FROM users WHERE ref = ?", (user_id,)
            ).fetchone()
            return result[0] if result else 0


async def add_user(message, referrer_id):
    username = f"@{message.from_user.username}" if message.from_user.username else None
    is_spartex = "spartex" in (message.from_user.full_name + username if username else '').lower()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, username, nick, ref, balance, bonus, sum, sessions, count_sessions, banned_users) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                message.from_user.id,
                username,
                message.from_user.full_name,
                referrer_id,
                0,
                5 if is_spartex else 0,
                0, 0, 0, 0
            ),
        )
        conn.commit()


async def update_data(message):
    username = f"@{message.from_user.username}" if message.from_user.username else None
    is_spartex = "spartex" in (message.from_user.full_name + username if username else '').lower()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, nick = ?, bonus = ? WHERE id = ?",
            (
                username,
                message.from_user.full_name,
                5 if is_spartex else 0,
                message.from_user.id,
            ),
        )
        conn.commit()


async def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]


async def check_balance(message):
    with get_connection() as conn:
        cursor = conn.cursor()
        balance = cursor.execute(
            "SELECT balance FROM users WHERE id = ?", (message,)
        ).fetchone()
        return balance[0] if balance else None


async def get_avg_balance():
    with get_connection() as conn:
        cursor = conn.cursor()
        balances = cursor.execute(
            "SELECT balance FROM users WHERE balance != 0"
        ).fetchall()
        if balances:
            return sum(balance[0] for balance in balances) / len(balances)
        return 0


async def get_all_users_with_balance():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE balance != 0")
        return [row[0] for row in cursor.fetchall()]


async def check_sessions(message):
    with get_connection() as conn:
        cursor = conn.cursor()
        sessions = cursor.execute(
            "SELECT sessions FROM users WHERE id = ?", (message,)
        ).fetchone()
        return sessions[0] if sessions else None


async def check_sessions_count(message):
    with get_connection() as conn:
        cursor = conn.cursor()
        count_sessions = cursor.execute(
            "SELECT count_sessions FROM users WHERE id = ?", (message,)
        ).fetchone()
        return count_sessions[0] if count_sessions else None


async def check_all_sessions_count():
    with get_connection() as conn:
        cursor = conn.cursor()
        session_counts = cursor.execute("SELECT count_sessions FROM users").fetchall()
        return sum(count[0] for count in session_counts)


async def check_avg_sessions_count():
    with get_connection() as conn:
        cursor = conn.cursor()
        session_counts = cursor.execute(
            "SELECT count_sessions FROM users WHERE count_sessions != 0"
        ).fetchall()
        if session_counts:
            return round(sum(count[0] for count in session_counts) / len(session_counts), 2)
        return 0


async def new_session(message, session):
    with get_connection() as conn:
        cursor = conn.cursor()
        count_sessions = cursor.execute(
            "SELECT count_sessions FROM users WHERE id = ?", (message,)
        ).fetchone()
        qq = int(count_sessions[0]) + 1 if count_sessions else 1

        if qq == 1:
            cursor.execute(
                "UPDATE users SET sessions = ? WHERE id = ?",
                (f"{qq}: {session}", message),
            )
        else:
            cursor.execute(
                "UPDATE users SET sessions = sessions || ? WHERE id = ?",
                (f", {qq}: {session}", message),
            )

        cursor.execute(
            "UPDATE users SET count_sessions = ? WHERE id = ?", (qq, message)
        )
        conn.commit()


async def update_sessions_in_db(user_id, session):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET sessions = ? WHERE id = ?", (session, user_id))
        conn.commit()


async def check_avg_wallets_count():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sessions FROM users")
        wallets = []
        for row in cursor.fetchall():
            matches = re.findall(r", (\d+):", row[0])
            wallets.extend(int(i) for i in matches)
        if wallets:
            return round(sum(wallets) / len(wallets), 2)
        return 0


async def check_project_count():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sessions FROM users")
        projects = []
        project_list = {"base", "linea", "scroll", "zora", "hyperlane"}
        for row in cursor.fetchall():
            words = set(re.findall(r"\b\w+\b", row[0]))
            projects.extend(words & project_list)

        project_counts = {project: projects.count(project) for project in project_list}
        total_count = sum(project_counts.values())
        if total_count != 0:
            percentages = {
                project: round((count / total_count) * 100, 2)
                for project, count in project_counts.items()
            }
            return percentages
        else:
            return 0


async def check_function_count():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sessions FROM users")
        functions = []
        functions_list = {"bridge", "swap", "protocol", "collector", "route"}
        for row in cursor.fetchall():
            words = set(re.findall(r"\b\w+\b", row[0]))
            functions.extend(words & functions_list)

        functions_counts = {func: functions.count(func) for func in functions_list}
        total_count = sum(functions_counts.values())
        if total_count != 0:
            percentages = {
                function: round((count / total_count) * 100, 2)
                for function, count in functions_counts.items()
            }
            return percentages
        else:
            return 0


async def ban_user(user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET banned_users = ? WHERE id = ?",
            (1, user_id),
        )
        conn.commit()


async def unban_user(user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET banned_users = ? WHERE id = ?",
            (0, user_id),
        )
        conn.commit()


async def is_user_banned(user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT banned_users FROM users WHERE id = ?", (user_id,)).fetchone()
        return result and result[0]


async def refill_balance(user_id: int, amount: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()[0]
        new_balance = balance + amount
        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, user_id),
        )
        conn.commit()


async def reduce_balance(user_id: int, amount):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()[0]
        new_balance = balance - amount
        print(new_balance)
        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, user_id),
        )
        conn.commit()
