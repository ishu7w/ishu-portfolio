// Factual, local answers for the existing animated portfolio conversation UI.
export function searchPortfolio(message, profile, projects) {
  const context = /^I'm looking at ([^.]+)\.\s*/i.exec(message);
  const query = (context ? message.slice(context[0].length) : message).trim();
  const lower = query.toLowerCase();
  const answer = text => ({ slug: '', text: text.slice(0, 390) });
  if (/\b(contact|email|reach|github|linkedin|leetcode)\b/.test(lower)) {
    return answer(`Email: ${profile.email}. GitHub: ${profile.links.github}. LinkedIn: ${profile.links.linkedin}. LeetCode: ${profile.links.leetcode}`);
  }
  if (/\b(skills|technologies|tech stack|tools|languages)\b/.test(lower)) {
    return answer(`${profile.name} builds with ${profile.skills.join(', ')}. He is learning Java and data structures, building full-stack projects and exploring applied AI.`);
  }
  if (/\b(internship|internships|recruit|hiring|collaborat|hackathon|opportunit)/.test(lower)) {
    return answer(`${profile.name} is interested in internships, practical software projects, open-source Java work and hackathon collaborations. Contact ${profile.email} or use the LinkedIn link in Contact.`);
  }
  if (!query || /^(hi|hello|hey)[! .]*$/i.test(query) || /\b(who are you|who is ishu|about (you|ishu)|introduce|background)\b/.test(lower)) {
    return answer(`${profile.name} is a ${profile.role}. He builds practical software with Java, TypeScript and React, explores applied AI, and contributes fixes to open-source Java tools. Explore the projects or ask about skills, contributions or contact.`);
  }
  const stop = new Set(['a', 'an', 'the', 'i', 'im', 'me', 'my', 'you', 'your', 'is', 'are', 'for', 'to', 'of', 'and', 'in', 'at', 'about', 'looking', 'show', 'find', 'please', 'project', 'projects', 'want', 'tell', 'more', 'work']);
  const terms = (lower.match(/[a-z0-9]+/g) || []).filter(word => !stop.has(word));
  let candidates = projects;
  if (/\b(contributions?|open source|merged|pull requests?)\b/.test(lower)) candidates = projects.filter(project => project.period === 'Merged contribution');
  else if (/\bjava\b/.test(lower) && /\bprojects?\b/.test(lower)) candidates = projects.filter(project => project.tags.includes('java') && project.period !== 'Merged contribution');
  const scored = candidates.map(project => {
    const title = project.name.toLowerCase();
    const tags = `${project.tags} ${project.clientName}`.toLowerCase();
    const text = `${title} ${tags} ${project.description}`.toLowerCase();
    const score = terms.reduce((total, term) => total + (title.includes(term) ? 8 : tags.includes(term) ? 3 : text.includes(term) ? 1 : 0), 0);
    return { project, score };
  }).sort((a, b) => b.score - a.score);
  const hit = scored[0];
  if (hit?.score) return { slug: hit.project.slug, text: `${hit.project.name}: ${hit.project.description}`.slice(0, 390) };
  const current = context && projects.find(project => project.slug === context[1]);
  if (current) return { slug: current.slug, text: `${current.name}: ${current.description}`.slice(0, 390) };
  return answer(`Explore ${profile.name}'s full-stack software, Java projects, applied AI, creative web work and merged open-source contributions. Try Parkwise, Credence, SmartHealth, ScholarAI, Checkstyle, skills or contact.`);
}
