import json
import re
import os
import datetime

cwd = os.getcwd()

START_DATE = datetime.datetime(2023, 12, 26, 0, 0)

def get_wjc_day(today):
  return (today - START_DATE).days

def addPM(pm, total):
  if pm == '-': pm = '0'
  if '+' in pm:
    _, pm = re.match('(\+)([0-9]+)', pm).groups()
  return total + int(pm)

def addTOI(toi, total):
  min, sec = re.match('([0-9]{1,2}):([0-5][0-9])', toi).groups()
  tot_min, tot_sec = re.match('([0-9]+):([0-5]{0,1}[0-9])', total).groups()
  sec = int(tot_sec) + int(sec)

  # If remainder, add to minutes and remove from seconds
  if sec > 60:
    sec -= 60
    min = str(int(min) + 1)
  
  if sec < 10:
    sec = '0' + str(sec)
  else:
    sec = str(sec)

  return str(int(tot_min) + int(min)) + ':' + sec

def validatePick(pick):
  KEYS = [
    "href",
    "team",
    "pos"
  ]

  for k in KEYS:
    if k not in pick.keys():
      print(f"\n### ERROR: Missing {k}")
      print()
      print(json.dumps(pick, indent=4))
      return False

  return True


def main():
  date = str(get_wjc_day(datetime.datetime.today()))

  with open(cwd + '/json/beta-wjc/2023-24/draft-picks.json', 'r') as json_file:
    draft_data = json.loads(json_file.read())

  with open(cwd + '/json/beta-wjc/2023-24/merged-player-data-day-'+date+'.json', 'r') as json_file:
    player_data = json.loads(json_file.read())

  md_file = open(cwd + '/ROSTERS.md', 'w')

  md_file.write("# Fantasy Rosters\n")

  ranking_data = {}

  for user in draft_data:
    roster = draft_data[user]
    player_map = {
      "F": [],
      "D": [],
      "G": []
    }

    g_total = 0
    a_total = 0
    pim_total = 0
    pm_total = 0
    sog_total = 0
    tpm_total = 0
    #toi_total = "0.00"

    gaa_list = []
    svp_list = []

    for pick in roster:

      try:

        if validatePick(player_data[pick]):

          href=player_data[pick]['href']
          pos=player_data[pick]['pos']
          team = player_data[pick]['team']


          if pos == "G":
            gaa=player_data[pick]['gaa']
            svp=player_data[pick]['svp']
            g=player_data[pick]['g']
            a=player_data[pick]['a']
            pim=player_data[pick]['pim']

            if re.match('[\d\.]+', gaa):
              gaa_list.append(float(gaa))
            else:
              gaa_list.append(100.0)
            if re.match('[\d\.]+', svp):
              svp_list.append(float(svp))
            else:
              svp_list.append(0.0)
            if re.match('\d+', g): g_total += int(g)
            if re.match('\d+', a): a_total += int(a)
            if re.match('\d+', pim): pim_total += int(pim)

            player_map[pos].append(
              f"| [{pick}]({href}) | {pos} | {team} | {g} | {a} | {pim} | {svp} | {gaa} |\n")
          else:
            g=player_data[pick]['g']
            a=player_data[pick]['a']
            pim=player_data[pick]['pim']
            pm=player_data[pick]['pm']
            sog=player_data[pick]['SOG']
            tpm=player_data[pick]['TPM']
            #toi = player_data['toi']

            if re.match('\d+', g): g_total += int(g)
            if re.match('\d+', a): a_total += int(a)
            if re.match('\d+', pim): pim_total += int(pim)
            pm_total = addPM(pm, pm_total)
            #if re.match('\-?\d+', pm): pm_total += int(pm)
            sog_total += sog
            tpm_total=round(tpm_total + tpm, 2)
            player_map[pos].append(
                f"| [{pick}]({href}) | {pos} | {team} | {g} | {a} | {sog} | {pim} | {pm} | {tpm} |\n")
      except:
        print(f"skipping (data): {pick}")

    ranking_data[user]={
      "Goals": g_total,
      "Assists": a_total,
      "Shots on Goal": sog_total,
      "Penalties in Minutes": pim_total,
      "Plus / Minus": pm_total,
      "Time Played in Minutes": round(tpm_total, 2),
      "Save Percentage": max(svp_list) if svp_list else '-',
      "Goals Against Average": min(gaa_list) if svp_list else '-'
    }

    md_file.write(f"## {user}\n")
    md_file.write(f"| Player | Pos | Team | G | A | SOG | PIM | +/- | TPM |\n")
    md_file.write(f"| :----- | --- | ---- | - | - | --- | --- | --- | --: |\n")


    skaters = player_map["F"]
    skaters.extend(player_map["D"])

    for sk in skaters:
      md_file.write(sk)

    md_file.write(
      f"| **Totals** | | | {g_total} | {a_total} | {sog_total} | {pim_total} | {pm_total} | {tpm_total} |\n")
    md_file.write(f"\n| Player | Pos | Team | G | A | PIM | S% | GAA |\n")
    md_file.write(f"| :----- | --- | ----| - | - | --- | -- | --: |\n")

    goalies=player_map["G"]
    for g in goalies:
      md_file.write(g)

  with open(cwd + '/json/beta-wjc/2023-24/standings.json', 'w') as json_file:
    json_file.write(json.dumps(ranking_data, indent=4))

  print(f'''
  Player data from /json/beta-wjc/2023-24/merged-player-data-day-{date}.json has been used to update ROSTERS.md
  Run `python src/beta-wjc/parse-standings.py` to update the STANDINGS.md file with this new data
  ''')


if __name__ == "__main__":
  main()
