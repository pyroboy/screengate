import{S as t,i as s,s as e,e as l,t as r,c as n,b as o,d as a,f as h,h as f,k as c,l as i,y as u,a as g,g as p,n as d,L as m}from"./index.0979fff8.js";function v(t,s,e){const l=t.slice();return l[1]=s[e],l}function b(t){let s,e,g,p,d=t[1].title+"";return{c(){s=l("li"),e=l("a"),g=r(d),this.h()},l(t){s=n(t,"LI",{});var l=o(s);e=n(l,"A",{rel:!0,href:!0});var r=o(e);g=a(r,d),r.forEach(h),l.forEach(h),this.h()},h(){f(e,"rel","prefetch"),f(e,"href",p="blog/"+t[1].slug)},m(t,l){c(t,s,l),i(s,e),i(e,g)},p(t,s){1&s&&d!==(d=t[1].title+"")&&u(g,d),1&s&&p!==(p="blog/"+t[1].slug)&&f(e,"href",p)},d(t){t&&h(s)}}}function x(t){let s,e,u,x,E,j=t[0],L=[];for(let s=0;s<j.length;s+=1)L[s]=b(v(t,j,s));return{c(){s=g(),e=l("h1"),u=r("Recent posts"),x=g(),E=l("ul");for(let t=0;t<L.length;t+=1)L[t].c();this.h()},l(t){s=p(t),e=n(t,"H1",{});var l=o(e);u=a(l,"Recent posts"),l.forEach(h),x=p(t),E=n(t,"UL",{class:!0});var r=o(E);for(let t=0;t<L.length;t+=1)L[t].l(r);r.forEach(h),this.h()},h(){document.title="Blog",f(E,"class","svelte-1frg2tf")},m(t,l){c(t,s,l),c(t,e,l),i(e,u),c(t,x,l),c(t,E,l);for(let t=0;t<L.length;t+=1)L[t].m(E,null)},p(t,[s]){if(1&s){let e;for(j=t[0],e=0;e<j.length;e+=1){const l=v(t,j,e);L[e]?L[e].p(l,s):(L[e]=b(l),L[e].c(),L[e].m(E,null))}for(;e<L.length;e+=1)L[e].d(1);L.length=j.length}},i:d,o:d,d(t){t&&h(s),t&&h(e),t&&h(x),t&&h(E),m(L,t)}}}function E({params:t,query:s}){return this.fetch("blog.json").then(t=>t.json()).then(t=>({posts:t}))}function j(t,s,e){let{posts:l}=s;return t.$set=(t=>{"posts"in t&&e(0,l=t.posts)}),[l]}export default class extends t{constructor(t){super(),s(this,t,j,x,e,{posts:0})}}export{E as preload};
