
import gql from 'graphql-tag';

// rat
// variable as params
// main mutaion = bio
export const ADD_TEACHER = gql`
mutation AddTeacher($name: String!, $position: String!,$idn: String!) {
	insert_bio(
		objects: {
			full_name: $name,
			id_number: $idn,
			teachers: { data: { position: $position } }
		}
	) {
		affected_rows
	}
}

`;



export const SCANS = gql`
query Rat2 {
  scanned(order_by: { created_at: desc }) {
    scan
  }
}
`;

export const NEW_SCANS = gql`
subscription Rat {
scanned(limit: 1, order_by: {created_at: desc}) {
scan
}
}
`;
