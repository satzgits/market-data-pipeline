import os
import time
from datetime import datetime


class Dashboard:
    def __init__(self, refresh_seconds=2):
        self.refresh_seconds = refresh_seconds
        self.latest_bars = {}
        self.recent_alerts = []

    def update_bar(self, symbol, row):
        self.latest_bars[symbol] = row

    def add_alert(self, alert):
        self.recent_alerts.append(alert)
        if len(self.recent_alerts) > 10:
            self.recent_alerts.pop(0)

    def render(self):
        os.system("cls" if os.name == "nt" else "clear")

        print("=" * 70)
        print("              MARKET DATA PIPELINE — Live Monitor")
        print("=" * 70)

        header = f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
        header += f"Symbols: {', '.join(self.latest_bars.keys())}"
        print(header)
        print("-" * 70)

        for symbol, row in self.latest_bars.items():
            close = row.get("close", 0)
            rsi = row.get("rsi", float("nan"))
            macd = row.get("macd_line", float("nan"))
            bb_u = row.get("bb_upper", float("nan"))
            bb_l = row.get("bb_lower", float("nan"))

            rsi_str = f"{rsi:.1f}" if not pd.isna(rsi) else "N/A"
            macd_str = f"{macd:+.1f}" if not pd.isna(macd) else "N/A"
            bb_u_str = f"${bb_u:.2f}" if not pd.isna(bb_u) else "N/A"
            bb_l_str = f"${bb_l:.2f}" if not pd.isna(bb_l) else "N/A"

            print(f"  {symbol:<10s}  Close: ${close:<8.2f}  "
                  f"RSI: {rsi_str:<6s}  MACD: {macd_str:<8s}")
            print(f"  {'':<10s}  BB Upper: {bb_u_str:<10s}  BB Lower: {bb_l_str:<10s}")
            print()

        if self.recent_alerts:
            print("─" * 70)
            print("  Recent Alerts:")
            for alert in self.recent_alerts[-5:]:
                print(f"  [{alert['time'].strftime('%H:%M:%S')}] {alert['message']}")

        print("=" * 70)
