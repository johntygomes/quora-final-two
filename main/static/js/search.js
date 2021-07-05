const search = document.getElementById("search");
const matchList = document.getElementById("match-list");

const searchStates = async (searchText) => {
  const res = await fetch("http://127.0.0.1:8000/api/question-list/");
  const states = await res.json();

  // Get Matches to current text inputData
  let matches = states.filter((state) => {
    // const regex = new RegExp(`^${searchText}`, "gi");
    // return state.title.match(regex) || state.body.match(regex);
    if (state.title.includes(searchText)) {
      return state.title;
    }
  });

  if (searchText.length === 0) {
    matches = [];
    matchList.innerHTML = "";
  }

  outputHtml(matches);
  // console.log(matches);
};

//Show Results In Html
const outputHtml = (matches) => {
  if (matches.length > 0) {
    const html = matches
      .map(
        (match) => `
      <div class = "card card-body mb-1">
        <h4><a href="http://127.0.0.1:8000/question/${match.id}" target="_blank">${match.title}</a></h4>
        <small>${match.body}</small>
      </div>
    `
      )
      .join("");
    console.log(html);
    matchList.innerHTML = html;
  }
};

search.addEventListener("input", () => searchStates(search.value));
