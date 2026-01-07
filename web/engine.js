const DiohodEngine = (() => {
  const MEMORY_LIMIT = 30;
  const TIME_LIMIT = 3500;

  class CompilationError extends Error {
    constructor(message) {
      super(message);
      this.name = "CompilationError";
      this.message = message;
    }
  }

  class ActionError extends Error {
    constructor(message) {
      super(message);
      this.name = "ActionError";
      this.message = message;
    }
  }

  class PlanetError extends Error {
    constructor(message) {
      super(message);
      this.name = "PlanetError";
      this.message = message;
    }
  }

  const Compass = {
    NORTH: 0,
    EAST: 1,
    SOUTH: 2,
    WEST: 3
  };

  const PlanetShape = {
    SQUARE: 0,
    TORUS: 1,
    X_CYLINDER: 2,
    Y_CYLINDER: 3
  };

  function artifact(description, alias, imgFile) {
    return {
      description,
      alias,
      img: imgFile ? `./img/artifacts/${imgFile}` : null
    };
  }

  const ARTIFACTS = {
    base: artifact("База", "base", "base.png"),
    dino: artifact("Динозавр", "dino", "dino.png"),
    cosmos: artifact("Тьма неопознанная", "cosmos", "cosmos.png"),
    volcano: artifact("Вулкан", "volcano", "volcano.png"),
    empty: artifact("Пустота", "empty", "empty.png"),
    camera_roll: artifact("Пленка кончилась", "camera_roll", "camera_roll.png"),
    idol: artifact("Истукан прямо, как на острове Пасхи", "idol", "idol.png"),

    ufo_01: artifact("НЛО-1", "ufo_01", "ufo_01.png"),
    ufo_02: artifact("НЛО-2", "ufo_02", "ufo_02.png"),
    ufo_03: artifact("НЛО-3", "ufo_03", "ufo_03.png"),
    key: artifact("Ключ", "key", "key.png"),
    gold: artifact("Золотишко", "gold", "gold.png"),

    mammoth: artifact("Мамонт", "mammoth", "mammoth.png"),
    goose: artifact("Гусь", "goose", "goose.png"),
    orangutan: artifact("Орангутан", "orangutan", "orangutan.png"),
    unicorn: artifact("Орангутан", "unicorn", "unicorn.png"),

    shard: artifact("Т", "shard", "shard.png"),
    letter_p: artifact("П", "letter_p", "letter_p.png"),
    letter_o: artifact("О", "letter_o", "letter_o.png"),
    letter_l: artifact("Л", "letter_l", "letter_l.png"),
    letter_e: artifact("Е", "letter_e", "letter_e.png"),
    letter_t: artifact("Т", "letter_t", "letter_t.png"),

    lenin: artifact("Памятник Ленину", "lenin", "lenin.png"),
    pyramid: artifact("Пирамида", "pyramid", "pyramid.png")
  };

  function randint(minIncl, maxIncl) {
    const min = Math.ceil(minIncl);
    const max = Math.floor(maxIncl);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function choice(arr) {
    if (!Array.isArray(arr) || arr.length === 0) {
      throw new Error("choice() expects non-empty array");
    }
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function preprocessLine(command) {
    let c = command.toLowerCase();
    c = c.trim();
    while (c.includes("  ")) c = c.replaceAll("  ", " ");
    return c;
  }

  function preprocessBlock(block) {
    let command = block.replaceAll("\t", "\n");
    while (command.includes("\n\n")) command = command.replaceAll("\n\n", "\n");
    return command;
  }

  function convertToLines(userProgram) {
    const program = preprocessBlock(userProgram);
    if (program.length > 20000) {
      throw new CompilationError("Программа слишком большая.");
    }
    const sendCommands = program.match(/send/g);
    if (sendCommands && sendCommands.length > 1) {
      throw new CompilationError("Каждый диоход может послать фото только 1 раз.");
    }
    const lines = program
      .split("\n")
      .map(preprocessLine)
      .filter((l) => l.length > 0);
    if (lines.length > 5000) {
      throw new CompilationError("Программа слишком большая.");
    }
    return lines;
  }

  function extractBlock(lines) {
    const text = lines.join("#");
    const stack = [];
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      if (ch === "{") stack.push(i);
      if (ch === "}") {
        if (stack.length === 0) {
          throw new CompilationError("Проверьте, правильно ли вы расставили скобки?");
        }
        if (stack.length === 1) {
          const open = stack.pop();
          const rawBlock = text.slice(open + 1, Math.max(open + 1, i - 1));
          const rawRemain = text.slice(i + 1);
          const blockLines = rawBlock
            .split("#")
            .map((s) => s.trim())
            .filter((s) => s.length > 0 && s !== "{");
          const remainLines = rawRemain
            .split("#")
            .map((s) => s.trim())
            .filter((s) => s.length > 0 && s !== "}");
          return { block: blockLines, remain: remainLines };
        }
        stack.pop();
      }
    }
    throw new CompilationError("Проверьте, правильно ли вы расставили скобки?");
  }

  function parseCycle(lines) {
    const hat = lines[0].replaceAll(" ", "").trim();
    const m = hat.match(/^repeat\((\d+)\)\{?$/);
    if (!m) {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    const amount = parseInt(m[1] || "", 10);
    if (!Number.isFinite(amount)) {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    const { block, remain } = extractBlock(lines);
    return { amount, body: block, remain };
  }

  function parseCondition(lines) {
    const hat = lines[0].trim();
    const m = hat.match(/^if\s+last\s+is\s+([a-zA-Z0-9_]+)\s*\{?$/);
    if (!m) {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    const alias = m[1].toLowerCase();
    const { block: trueBlock, remain } = extractBlock(lines);

    if (remain.length > 0 && remain[0].trim().startsWith("else")) {
      const elseHat = remain[0].trim();
      if (!/^else\s*\{?$/.test(elseHat)) {
        throw new CompilationError(`Проблема в строке \`\`\`\"${elseHat}\"\`\`\``);
      }
      const { block: falseBlock, remain: remain2 } = extractBlock(remain);
      return { alias, trueBlock, falseBlock, remain: remain2 };
    }

    return { alias, trueBlock, falseBlock: [], remain };
  }

  function parsePop(lines) {
    const hat = lines[0].replaceAll(" ", "").trim();
    if (hat !== "pop()") {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    return { remain: lines.slice(1) };
  }

  function parsePhoto(lines) {
    const hat = lines[0].replaceAll(" ", "").trim();
    if (hat !== "photo()") {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    return { remain: lines.slice(1) };
  }

  function parseMove(lines) {
    const hat = lines[0].replaceAll(" ", "").trim();
    if (hat !== "move()") {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    return { remain: lines.slice(1) };
  }

  function parseRotate(lines) {
    const hat = lines[0].replaceAll(" ", "").trim().toLowerCase();
    const m = hat.match(/^rotate\((|north|east|west|south)\)$/);
    if (!m) {
      throw new CompilationError(`Проблема в строке \`\`\`\"${hat}\"\`\`\``);
    }
    const directionText = m[1];
    const direction =
      {
        north: Compass.NORTH,
        west: Compass.WEST,
        east: Compass.EAST,
        south: Compass.SOUTH,
        "": null
      }[directionText] ?? null;
    return { direction, remain: lines.slice(1) };
  }

  class Planet {
    constructor({ width, height, base_x, base_y, shape, missionText }) {
      this.width = width;
      this.height = height;
      this.base_x = base_x;
      this.base_y = base_y;
      this.shape = shape;
      this.missionText = missionText;
      this.area = Array.from({ length: width }, () => Array.from({ length: height }, () => null));
      this.area[base_x][base_y] = ARTIFACTS.base;
    }

    getAllObjectsCells() {
      const all = [];
      for (let i = 0; i < this.width; i++) {
        for (let j = 0; j < this.height; j++) {
          if (this.area[i][j] != null) all.push([i, j]);
        }
      }
      return all;
    }
  }

  class Shuttle {
    constructor(planet) {
      this.planet = planet;
      this.direction = Compass.NORTH;
      this.x = planet.base_x;
      this.y = planet.base_y;
      this.memory = [];
      this.exploredCells = new Set();
      this.notPhotographed = planet.getAllObjectsCells();
      this.time = 0;
    }

    execute(lines) {
      let current = Array.isArray(lines) ? lines.slice() : [];

      while (current.length > 0) {
        if (this.time > TIME_LIMIT) {
          throw new ActionError('"Я слишком долго на этой планете - села батарея. Прощайте!"');
        }

        const head = current[0];

        if (head.includes("repeat")) {
          const cycle = parseCycle(current);
          for (let i = 0; i < cycle.amount; i++) {
            this.execute(cycle.body);
          }
          current = cycle.remain;
          continue;
        }

        if (head.includes("if")) {
          const condition = parseCondition(current);
          if (this.memory.length === 0) {
            throw new CompilationError("В памяти нет фото. Невозможно проверить условие!");
          }
          const lastPhoto = this.memory[this.memory.length - 1];
          if (lastPhoto.alias === condition.alias) {
            this.execute(condition.trueBlock);
          } else {
            this.execute(condition.falseBlock);
          }
          current = condition.remain;
          continue;
        }

        if (head.includes("photo")) {
          const photo = parsePhoto(current);
          if (this.memory.length < MEMORY_LIMIT) {
            const [nx, ny] = this._getCoordinate();
            const photography = this._makePhoto(nx, ny);
            if (photography.alias !== "cosmos") {
              this.exploredCells.add(`${nx},${ny}`);
            }
            this.memory.push(photography);
            this.notPhotographed = this.notPhotographed.filter(([x, y]) => !(x === nx && y === ny));
          }
          if (this.memory.length === MEMORY_LIMIT) {
            this.memory.push(ARTIFACTS.camera_roll);
          }
          this.time += 1;
          current = photo.remain;
          continue;
        }

        if (head.includes("rotate")) {
          const rotate = parseRotate(current);
          if (rotate.direction != null) {
            this.direction = rotate.direction;
          } else {
            this.direction = {
              [Compass.NORTH]: Compass.EAST,
              [Compass.WEST]: Compass.NORTH,
              [Compass.EAST]: Compass.SOUTH,
              [Compass.SOUTH]: Compass.WEST
            }[this.direction];
          }
          this.time += 1;
          current = rotate.remain;
          continue;
        }

        if (head.includes("move")) {
          const move = parseMove(current);
          const [nx, ny] = this._getCoordinate();
          const photo = this._makePhoto(nx, ny);
          if (photo.alias === "cosmos") {
            throw new PlanetError("Связь с диоходом потеряна!");
          }
          if (photo.alias === "dino") {
            throw new ActionError('"На планете обнаружен диноза..."');
          }
          if (photo.alias === "volcano") {
            throw new ActionError('"Зря я сюда пошёл: тут был вулкан. Прощайте!"');
          }
          this.x = nx;
          this.y = ny;
          this.time += 1;
          current = move.remain;
          continue;
        }

        if (head.includes("pop")) {
          const pop = parsePop(current);
          if (this.memory.length === 0) {
            throw new CompilationError("Не могу удалить фото - память пуста.");
          }
          this.memory.pop();
          if (this.memory.length === MEMORY_LIMIT) {
            this.memory.pop();
          }
          this.time += 1;
          current = pop.remain;
          continue;
        }

        throw new CompilationError(`Команда \`\`\`\"${head}\"\`\`\` не распознана`);
      }
    }

    _makePhoto(x, y) {
      if (x < 0 || x >= this.planet.width) return ARTIFACTS.cosmos;
      if (y < 0 || y >= this.planet.height) return ARTIFACTS.cosmos;
      if (this.planet.area[x][y] == null) return ARTIFACTS.empty;
      this.time += 1;
      return this.planet.area[x][y];
    }

    _getCoordinate() {
      const delta = {
        [Compass.WEST]: [-1, 0],
        [Compass.EAST]: [1, 0],
        [Compass.NORTH]: [0, 1],
        [Compass.SOUTH]: [0, -1]
      };
      let nx = this.x + delta[this.direction][0];
      let ny = this.y + delta[this.direction][1];

      if (this.planet.shape === PlanetShape.TORUS || this.planet.shape === PlanetShape.X_CYLINDER) {
        nx = ((nx % this.planet.width) + this.planet.width) % this.planet.width;
      }
      if (this.planet.shape === PlanetShape.TORUS || this.planet.shape === PlanetShape.Y_CYLINDER) {
        ny = ((ny % this.planet.height) + this.planet.height) % this.planet.height;
      }
      return [nx, ny];
    }
  }

  function createPlanets() {
    const planets = {};

    const planet01 = new Planet({
      width: 5,
      height: 5,
      base_x: 1,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_01"
    });
    planet01.area[2][1] = ARTIFACTS.idol;
    planets.planet_01 = planet01;

    const planet02 = new Planet({
      width: 5,
      height: 5,
      base_x: 2,
      base_y: 2,
      shape: PlanetShape.SQUARE,
      missionText: "planet_02"
    });
    planet02.area[3][2] = ARTIFACTS.ufo_01;
    planet02.area[2][3] = ARTIFACTS.ufo_02;
    planet02.area[1][2] = ARTIFACTS.ufo_03;
    planets.planet_02 = planet02;

    const planet03 = new Planet({
      width: 3,
      height: 778,
      base_x: 1,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_03"
    });
    planet03.area[1][777] = ARTIFACTS.key;
    planets.planet_03 = planet03;

    const planet04 = new Planet({
      width: 6,
      height: 6,
      base_x: 0,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_04"
    });
    planet04.area[5][1] = ARTIFACTS.gold;
    planets.planet_04 = planet04;

    const planet05 = new Planet({
      width: 4,
      height: 4,
      base_x: 0,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_05"
    });
    planet05.area[0][randint(1, 3)] = ARTIFACTS.mammoth;
    planet05.area[1][0] = ARTIFACTS.orangutan;
    planet05.area[2][randint(1, 2)] = ARTIFACTS.goose;
    planet05.area[3][0] = ARTIFACTS.unicorn;
    planets.planet_05 = planet05;

    const planet06 = new Planet({
      width: 1,
      height: 1000,
      base_x: 0,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_06"
    });
    planet06.area[0][randint(1, 150)] = ARTIFACTS.shard;
    planet06.area[0][randint(151, 300)] = ARTIFACTS.letter_e;
    planet06.area[0][randint(301, 450)] = ARTIFACTS.letter_l;
    planet06.area[0][randint(451, 600)] = ARTIFACTS.letter_o;
    planet06.area[0][randint(601, 750)] = ARTIFACTS.letter_p;
    planet06.area[0][randint(751, 1000)] = ARTIFACTS.letter_t;
    planets.planet_06 = planet06;

    const planet07 = new Planet({
      width: 3,
      height: 100,
      base_x: 1,
      base_y: 0,
      shape: PlanetShape.SQUARE,
      missionText: "planet_07"
    });
    planet07.area[1][randint(1, 75)] = ARTIFACTS.dino;
    planet07.area[1][84] = ARTIFACTS.lenin;
    planets.planet_07 = planet07;

    const planet08 = new Planet({
      width: 5,
      height: 5,
      base_x: 2,
      base_y: 2,
      shape: PlanetShape.SQUARE,
      missionText: "planet_08"
    });
    const dinoCoord = choice([
      [2, 3],
      [2, 1],
      [3, 2],
      [1, 2]
    ]);
    planet08.area[dinoCoord[0]][dinoCoord[1]] = ARTIFACTS.dino;
    planet08.area[0][1] = ARTIFACTS.pyramid;
    planets.planet_08 = planet08;

    const planet09 = new Planet({
      width: 3,
      height: 4,
      base_x: 1,
      base_y: 0,
      shape: PlanetShape.Y_CYLINDER,
      missionText: "planet_09"
    });
    planet09.area[2][0] = ARTIFACTS.volcano;
    planet09.area[0][1] = ARTIFACTS.volcano;
    planet09.area[1][3] = ARTIFACTS.volcano;
    planet09.area[2][3] = ARTIFACTS.volcano;
    planets.planet_09 = planet09;

    return planets;
  }

  function runMission({ missionId, program }) {
    const planetKeyByMission = {
      MISSION_01: "planet_01",
      MISSION_02: "planet_02",
      MISSION_03: "planet_03",
      MISSION_04: "planet_04",
      MISSION_05: "planet_05",
      MISSION_06: "planet_06",
      MISSION_07: "planet_07",
      MISSION_08: "planet_08",
      MISSION_09: "planet_09"
    };

    const key = planetKeyByMission[missionId];
    if (!key) {
      throw new Error(`Unknown missionId: ${missionId}`);
    }

    const planets = createPlanets();
    const planet = planets[key];

    const lines = convertToLines(program);
    const shuttle = new Shuttle(planet);
    shuttle.execute(lines);

    const uniqueAmount = shuttle.exploredCells.size;
    let text = "Диоход завершил свою миссию!\n";
    text += `Cфотографировано различных клеток планеты: ${uniqueAmount} шт.\n`;
    if (shuttle.memory.length === 0) {
      text += "Не было получено ни одной фотографии";
    } else {
      text += "Были получены следующие фотографии:";
    }

    return {
      text,
      photos: shuttle.memory.map((a) => ({ alias: a.alias, description: a.description, img: a.img }))
    };
  }

  return {
    runMission,
    errors: {
      CompilationError,
      ActionError,
      PlanetError
    }
  };
})();

window.DiohodEngine = DiohodEngine;
