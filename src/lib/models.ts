// Session type matching the firebase document fields
export interface Club {
  id: string;
  name: string;
  public?: boolean;
  sessions?: any;
  beers?: any;
};

export interface Session {
  id?: string;
  club: string;
  number: number;
  date: string;
  location: string;
  winner?: string;
  beer?: string;
  brewery?: string;
  avg_abv?: number;
  count?: number;
  photos?: string[];
  recap?: string;
};

// Beer type matching the firebase document fields
export interface Beer {
  id?: string;
  session: number;
  name: string;
  brewery: string;
  abv: number;
  style: string;
  type: string;
  club: string;
  order: string;
  score: number;
  win: boolean;
  user: string;
};

export interface MemberData {
  wins: number,
  avg_score: number,
  avg_abv: number,
  count: number,
  win_rate: number
}

// Member type matching the firebase document fields
export interface Member {
  id: string;
  name?: string;
  full_name: string;
  email: string;
  photoURL: string;
  notes?: object;
  roles: Roles;
  clubs: string[];
  data: { [id: string]: MemberData };
};

export interface Roles {
  admin: boolean;
  editor: boolean;
  viewer: boolean;
};

export const userDefaults: Member = {
  id: null,
  name: null,
  full_name: null,
  email: null,
  photoURL: null,
  notes: {},
  roles: {
    admin: false,
    editor: true,
    viewer: true
  },
  clubs: [],
  data: {}
};

export const beerDefaults: Beer = {
  id: '',
  session: null,
  name: '',
  brewery: '',
  abv: null,
  style: '',
  type: '',
  club: '',
  order: '',
  score: null,
  win: false,
  user: ''
};

export const sessionDefaults: Session = {
  id: '',
  club: '',
  number: null,
  date: '',
  location: ''
};

// Information on how to display sessions in a table
export const sessionView = [
  { key: 'number', text: 'Session', width: 100, show: (session: Session) => session.number },
  { key: 'date', text: 'Date', width: 100, show: (session: Session) => session.date },
  { key: 'winner', text: 'Winner', width: 120, show: (session: Session) => session.winner ?? '' },
  { key: 'location', text: 'Location', width: 120, show: (session: Session) => session.location ?? '' },
  { key: 'beer', text: 'Winning Beer', width: 180, show: (session: Session) => session.beer ?? '' },
  { key: 'brewery', text: 'Brewery', width: 180, show: (session: Session) => session.brewery ?? '' },
  { key: 'count', text: 'Entries', width: 100, show: (session: Session) => session.count ?? '' },
  { key: 'avg_abv', text: 'Avg ABV', width: 120, show: (session: Session) => (session.avg_abv ? session.avg_abv.toFixed(1) : '') }
];

// Information on how to display beers in a table
export const beerView = [
  { key: 'session', text: 'Session', width: 100, show: (beer: Beer) => beer.session },
  { key: 'name', text: 'Name', width: 180, show: (beer: Beer) => beer.name ?? '' },
  { key: 'brewery', text: 'Brewery', width: 180, show: (beer: Beer) => beer.brewery ?? '' },
  { key: 'type', text: 'Style', width: 180, show: (beer: Beer) => beer.type ?? '' },
  { key: 'abv', text: 'ABV', width: 100, show: (beer: Beer) => beer.abv ?? '' },
  { key: 'score', text: 'Votes', width: 100, show: (beer: Beer) => beer.score ?? '' },
  { key: 'win', text: 'Result', width: 100, show: (beer: Beer) => beer.win ? 'Win' : '' },
  { key: 'user', text: 'Member', width: 120, show: (beer: Beer) => beer.user ?? '' }
];

function makeDataFormatter(parameter: string, float: undefined | number = undefined): (member: Member, club: string) => string {
  return (member: Member, club: string) => {
    if (!member.data[club] || !member.data[club][parameter]) {
      return '';
    }
    if (float == undefined) {
      return member.data[club][parameter];
    } else {
      return member.data[club][parameter].toFixed(float);
    }
  }
}

// Information on how to display members in a table
export const memberView = [
  { key: 'name', text: 'Member', width: 120, show: (member: Member, club: string) => member.name ?? '' },
  { key: 'wins', text: 'Wins', width: 100, show: makeDataFormatter('wins') },
  { key: 'count', text: 'Beers', width: 100, show: makeDataFormatter('count') },
  { key: 'avg_abv', text: 'Avg ABV', width: 120, show: makeDataFormatter('avg_abv', 1) },
  { key: 'avg_score', text: 'Avg Score', width: 120, show: makeDataFormatter('avg_score', 1) },
  { key: 'win_rate', text: 'Win Rate', width: 120, show: makeDataFormatter('win_rate', 3) },
  { key: 'full_name', text: 'Google Name', width: 180, show: (member: Member, club: string) => member.full_name },
  { key: 'email', text: 'Email', width: 220, show: (member: Member, club: string) => member.email }
];

export const memberCompare: {[key: string]: (member: Member, club: string) => any } = {
  name: (member, club) => member.name,
  wins: (member, club) => member.data[club].wins,
  count: (member, club) => member.data[club].count,
  avg_abv: (member, club) => member.data[club].avg_abv,
  avg_score: (member, club) => member.data[club].avg_score,
  win_rate: (member, club) => member.data[club].win_rate,
  full_name: (member, club) => member.full_name,
  email: (member, club) => member.email
}
export const roleView = [
  {
    key: 'admin', text: 'Admin', width: 70, show: (member: Member) => member.roles.admin,
    disable: (member: Member, user: Member) => (member.id == user.id)
  },
  {
    key: 'editor', text: 'Editor', width: 70, show: (member: Member) => member.roles.editor,
    disable: (member: Member, user: Member) => (member.roles.admin || member.id == user.id)
  },
  {
    key: 'viewer', text: 'Viewer', width: 70, show: (member: Member) => member.roles.viewer,
    disable: (member: Member, user: Member) => (member.roles.editor || member.id == user.id)
  }
];

export function sessionsToCsv(sessions: Session[]) {
  const keys = sessionView.map(item => item.key);
  downloadCsv('sessions.csv', keys, sessions);
}

export function beersToCsv(beers: Beer[]) {
  const keys = beerView.map(item => item.key);
  // These keys are in the data type but displayed, so need to add manually
  keys.push('order', 'style');
  downloadCsv('beers.csv', keys, beers);
}

export function membersToCsv(members: Member[]) {
  const keys = memberView.map(item => item.key);
  downloadCsv('members.csv', keys, members);
}

function downloadCsv(filename: string, keys: Array<string>, data: Array<object>) {
  // Join the data into csv format with a header
  const dataText = data.map(data => keys.map(key => data[key]).join(',')).join('\n');
  const csvText = [keys.join(','), dataText].join('\n');

  // This makes the browser "download" a file from the text string created
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csvText));
  element.setAttribute('download', filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}