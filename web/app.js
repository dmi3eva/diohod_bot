const MISSIONS = [
  {
    id: "MISSION_01",
    title: "Миссия 1",
    badge: "01",
    img: "./img/missions/planet_01.png",
    text: `На снимках с телескопа видно, что на этой планете располагается неопознанный объект.\n\nСфотографируйте его, добравшись до квадрата, помеченного знаком сюрприза.\n\nНе забудьте опубликовать новость.\n\nОсторожно! Не свалитесь с планеты! Похоже, она плоская и имеет форму квадрата 5 на 5.\n\nПрограмму пишите прямо в сообщении.`
  },
  {
    id: "MISSION_02",
    title: "Миссия 2",
    badge: "02",
    img: "./img/missions/planet_02.png",
    text: `Базу на планете №2 окружили летающие тарелки. Надо понять, какова угроза?\n\nИтак, известно, что на каких-то из четырех соседних по стороне клеток находятся НЛО.\n\nВаша миссия — узнать, сколько их.`
  },
  {
    id: "MISSION_03",
    title: "Миссия 3",
    badge: "03",
    img: "./img/missions/planet_03.png",
    text: `На планете №3 на расстоянии ровно 777 клеток (прямо на краю света) находится объект, который в своей жизни искал каждый.\n\nУзнайте, что это, и не свалитесь с планеты. Опасно!`
  },
  {
    id: "MISSION_04",
    title: "Миссия 4",
    badge: "04",
    img: "./img/missions/planet_04.png",
    text: `Известно, что на планете №4 где-то в желтой зоне находится золотое месторождение.\n\nОпределите его координаты, если база находится в точке (0, 0).\n\nПостарайтесь написать максимально короткую программу.`
  },
  {
    id: "MISSION_05",
    title: "Миссия 5",
    badge: "05",
    img: "./img/missions/planet_05.png",
    text: `Планета №5 плоская, имеет размер 4 на 4 клеточки и базу в точке (0,0). Самое главное — по ней бродят животные!!!\n\nОбойдите всю планету и найдите всех!\n\nИмейте в виду — животные медленно, но перемещаются. После каждого нового пуска диохода животные будут оказываться в новых местах.`
  },
  {
    id: "MISSION_06",
    title: "Миссия 6",
    badge: "06",
    img: null,
    text: `Давным-давно на планете №6 произошло крушение ракеты. Теперь на планете полно осколков.\n\nПопробуйте понять, как называлась разбившаяся ракета.\n\nКоординаты базы: (0, 0). Планета плоская и имеет форму квадрата 1 на 1000.\n\nИмейте в виду — на планете дует сильный ветер и осколки перемещаются.\n\nПамять фотоаппарата позволяет сохранить только 30 кадров.`
  },
  {
    id: "MISSION_07",
    title: "Миссия 7",
    badge: "07",
    img: "./img/missions/planet_07.png",
    text: `По снимкам из космоса видно, что на планете №7 где-то на одной вертикали с базой (к северу от неё) находится неопознанный монументальный объект.\n\nПопробуйте опознать его.\n\nВнимание! По этой же вертикали бегает динозавр. Встречи с ним диоход не переживет.\n\nРазмер планеты: 3 на 100. База находится в точке (1, 0).`
  },
  {
    id: "MISSION_08",
    title: "Миссия 8",
    badge: "08",
    img: "./img/missions/planet_08.png",
    text: `В зоне по периметру планеты №8 располагается некий огромный объект.\n\nОпределите, что это?\n\nПо серой зоне бегает динозавр. Встреться с ним не хотелось бы (мягко говоря).\n\nРазмер планеты: 5 на 5. База находится в точке (2, 2).`
  },
  {
    id: "MISSION_09",
    title: "Миссия 9",
    badge: "09",
    img: null,
    text: `Самая далекая и самая интересная планета. Про нее неизвестно НИЧЕГО. Исследуйте её. Подробно опишите результаты и свои гипотезы.`
  }
];

const HELP_TEXT = `
- Планета разбита на клетки. В каждой клетке не более одного объекта
- Начальное положение диохода: база, направление — север
- В конце каждой миссии диоход отправляет нам все сделанные фотографии
- move() — сдвинуться на одну клетку в направлении головы
- rotate() — повернуться на 90 градусов по часовой стрелке
- rotate(WEST) — повернуться на запад
- photo() — сделать фотографию
- pop() — удалить последнюю фотографию

Повторить 4 раза:
repeat(4)
{
  <ДЕЙСТВИЯ ДЛЯ ПОВТОРЕНИЯ>
}

Если на последней фотографии ВУЛКАН:
if last is VOLCANO
{
  <Что делать, если условие выполнено?>
}
else
{
  <Что делать, если условие не выполнено?>
}
`;

const els = {
  missionsList: document.getElementById("missionsList"),
  missionText: document.getElementById("missionText"),
  missionImg: document.getElementById("missionImg"),
  missionImgPlaceholder: document.getElementById("missionImgPlaceholder"),
  code: document.getElementById("code"),
  startBtn: document.getElementById("startBtn"),
  helpBtn: document.getElementById("helpBtn"),
  modal: document.getElementById("modal"),
  modalTitle: document.getElementById("modalTitle"),
  modalBody: document.getElementById("modalBody"),
  modalOk: document.getElementById("modalOk"),
  modalClose: document.getElementById("modalClose")
};

let activeMissionId = "MISSION_01";

function escapeHtml(s) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setActiveMission(missionId) {
  activeMissionId = missionId;
  const mission = MISSIONS.find((m) => m.id === missionId) ?? MISSIONS[0];

  for (const node of els.missionsList.querySelectorAll(".mission")) {
    node.classList.toggle("mission--active", node.dataset.id === missionId);
  }

  els.missionText.innerHTML = escapeHtml(mission.text).replaceAll("\n", "<br />");

  if (mission.img) {
    els.missionImg.src = mission.img;
    els.missionImg.onload = () => {
      els.missionImg.style.display = "block";
      els.missionImgPlaceholder.style.display = "none";
    };
    els.missionImg.onerror = () => {
      els.missionImg.style.display = "none";
      els.missionImgPlaceholder.style.display = "block";
    };
  } else {
    els.missionImg.style.display = "none";
    els.missionImgPlaceholder.style.display = "none";
  }
}

function renderMissions() {
  els.missionsList.innerHTML = "";
  for (const m of MISSIONS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "mission";
    btn.dataset.id = m.id;
    btn.innerHTML = `
      <span class="mission__name">${escapeHtml(m.title)}</span>
      <span class="mission__badge">${escapeHtml(m.badge)}</span>
    `;
    btn.addEventListener("click", () => setActiveMission(m.id));
    els.missionsList.appendChild(btn);
  }
}

function openModal(title, bodyHtml) {
  els.modalTitle.textContent = title;
  els.modalBody.innerHTML = bodyHtml;
  els.modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
  els.modal.setAttribute("aria-hidden", "true");
  els.modalBody.innerHTML = "";
}

function setStartLoading(isLoading) {
  els.startBtn.disabled = isLoading;
  els.startBtn.textContent = isLoading ? "Выполняю…" : "Запустить миссию";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function handleStart() {
  const mission = MISSIONS.find((m) => m.id === activeMissionId) ?? MISSIONS[0];
  const code = (els.code.value || "").trim();

  if (!window.DiohodEngine || typeof window.DiohodEngine.runMission !== "function") {
    openModal(
      "Ошибка",
      "Движок выполнения миссий не загружен. Обновите страницу или проверьте, что engine.js доступен."
    );
    return;
  }

  if (code.length > 20000) {
    openModal("Отчёт о полёте", "Программа слишком большая.");
    return;
  }

  (async () => {
    setStartLoading(true);
    openModal(
      "Отчёт о полёте",
      "<div style=\"color: rgba(255,255,255,0.78);\">Выполняю программу…</div>"
    );
    await sleep(0);

    try {
      const result = window.DiohodEngine.runMission({
        missionId: activeMissionId,
        program: code
      });

    const photos = Array.isArray(result.photos) ? result.photos : [];
    const gallery =
      photos.length > 0
        ? `<div style="margin-top: 12px;">
            <div style="margin-bottom: 10px; color: rgba(255,255,255,0.75);">Фотографии:</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px;">
              ${photos
                .map((p, idx) => {
                  const src = p.img ? escapeHtml(p.img) : "";
                  const caption = escapeHtml(p.description || p.alias || "");
                  const timeLabel = `t=${idx + 1}`;
                  return `
                    <div style="border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; overflow: hidden; background: rgba(0,0,0,0.18);">
                      ${src ? `<div style="position: relative; background: #ffffff;">
                        <div style="position: absolute; top: 8px; left: 8px; padding: 2px 8px; border-radius: 999px; font-size: 12px; background: rgba(0,0,0,0.7); color: #ffffff;">${timeLabel}</div>
                        <img src="${src}" alt="${caption}" style="width: 100%; height: 110px; object-fit: contain; display: block; background: #ffffff;" />
                      </div>` : ""}
                      <div style="padding: 8px; font-size: 12px; color: rgba(255,255,255,0.78);">
                        <div style="margin-bottom: 4px; color: rgba(255,255,255,0.62);">${timeLabel}</div>
                        <div>${caption}</div>
                      </div>
                    </div>
                  `;
                })
                .join("")}
            </div>
          </div>`
        : "";

    const body = `
      <div style="margin-bottom: 10px; color: rgba(255,255,255,0.7);">
        Выбранная миссия: <span class="kbd">${escapeHtml(mission.title)}</span>
      </div>
      <pre style="white-space: pre-wrap; margin: 0; padding: 12px; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; background: rgba(0,0,0,0.18);">${escapeHtml(
        (result.text || "").trim()
      )}</pre>
      ${gallery}
    `;

      openModal("Отчёт о полёте", body);
    } catch (err) {
      const message = err && err.message ? String(err.message) : "Ошибка в программе";
      const body = `
        <div style="margin-bottom: 10px; color: rgba(255,255,255,0.7);">
          Выбранная миссия: <span class="kbd">${escapeHtml(mission.title)}</span>
        </div>
        <pre style="white-space: pre-wrap; margin: 0; padding: 12px; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; background: rgba(0,0,0,0.18);">${escapeHtml(
          message
        )}</pre>
      `;
      openModal("Отчёт о полёте", body);
    } finally {
      setStartLoading(false);
    }
  })();
}

function initModal() {
  els.modal.addEventListener("click", (e) => {
    if (e.target && e.target.dataset && e.target.dataset.close === "true") {
      closeModal();
    }
  });

  els.modalOk.addEventListener("click", closeModal);
  els.modalClose.addEventListener("click", closeModal);

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && els.modal.getAttribute("aria-hidden") === "false") {
      closeModal();
    }
  });
}

function init() {
  renderMissions();
  initModal();

  setActiveMission(activeMissionId);

  els.helpBtn.addEventListener("click", () => {
    openModal(
      "Справка",
      `<pre style="white-space: pre-wrap; margin: 0; padding: 12px; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; background: rgba(0,0,0,0.18);">${escapeHtml(HELP_TEXT.trim())}</pre>`
    );
  });

  els.startBtn.addEventListener("click", handleStart);
}

init();
