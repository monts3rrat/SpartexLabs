import cli from "cli";
import { CONFIG } from "./config";
import { WALLETS_FILENAME, CSV_DELIMITER, CSV_RESULTS_FOLDER } from "./constants";
import { chooseNetwork } from "./modules/choice";
import Cvs from "./modules/csv";
import { getErc20Balance } from "./modules/erc20";
import { getNativeBalance } from "./modules/native";
import { Network } from "./types";
import { getAddressFromWallet, loadFormFile } from "./utils";
import fs from "fs";
import { exec } from "child_process";
import fs, {WriteStream} from "fs";
import path from "path";

export default class Csv {
private stream: WriteStream;

  constructor(network: Network) {
    this.stream = fs.createWriteStream(
      path.join(CSV_RESULTS_FOLDER, network + ".csv"),
    );
  }

  write(data: (string | number)[]) {
    const line = data.join(CSV_DELIMITER) + "\n";
    this.stream.write(line);
  }

  close() {
    this.stream.close();
  }
}

const wallets = await loadFormFile(WALLETS_FILENAME);
const addresses = wallets.map(getAddressFromWallet);
const isWalletsContainPrivateKeys = wallets.some((wallet) =>
wallet.length > 42
);

const networkArg = process.argv[2] as Network;
let network = networkArg;


if (!network) {
  network = await chooseNetwork();
}

const columns = CONFIG[network].COLUMNS;

let csv = new Csv(network);

try {
 processCSVData(csv, network, columns, wallets, addresses, isWalletsContainPrivateKeys);
} catch (error) {
 console.error('Error processing CSV data:', error);
}


async function processCSVData(csv: Csv, network: Network, columns: string[], wallets: string[], addresses: string[], isWalletsContainPrivateKeys: boolean) {
  const data = await Promise.all(
    columns.map((token) => {
      if (token === "native") {
        return getNativeBalance(network, addresses);
      }

      return getErc20Balance(network, addresses, token);
    }),
  );

  const walletColumns = isWalletsContainPrivateKeys
    ? ["Address", "PrivateKey"]
    : ["Address"];
  const csvHeader = [...walletColumns, ...data.map((item) => item.header)];
  csv.write(csvHeader);

  for (let i = 0; i < wallets.length; i++) {
    const wallet = wallets[i];
    const address = addresses[i];

    const privateKey = wallet !== address ? wallet : "";
    const walletColumns = isWalletsContainPrivateKeys
      ? [address, privateKey]
      : [address];
    const row = [...walletColumns, ...data.map((item) => item.balances[i])];

    csv.write(row);
  }

  csv.close();
  cli.spinner("Готово", true);
}