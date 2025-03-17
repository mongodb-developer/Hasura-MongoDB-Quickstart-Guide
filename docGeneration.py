import requests
import os

HASURA_ENDPOINT = os.getenv('HASURA_ENDPOINT', 'http://localhost:8080/v1/graphql')
HASURA_ADMIN_SECRET = os.getenv('HASURA_ADMIN_SECRET', 'your-secret')
OUTPUT_FILE = 'GRAPHQL_SCHEMA_DOCS.md'

introspection_query = """
query IntrospectionQuery {
  __schema {
    types {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
}
"""

def fetch_graphql_schema():
    headers = {'x-hasura-admin-secret': HASURA_ADMIN_SECRET}
    response = requests.post(HASURA_ENDPOINT, json={'query': introspection_query}, headers=headers)
    response.raise_for_status()
    return response.json()['data']['__schema']


def generate_markdown(schema):
    md = '# GraphQL Schema Documentation\n\n'
    for gql_type in schema['types']:
        if gql_type['fields'] and not gql_type['name'].startswith('__'):
            md += f"## {gql_type['name']} ({gql_type['kind']})\n"
            if gql_type['description']:
                md += f"_{gql_type['description']}_\n"
            md += '\n'

            for field in gql_type['fields']:
                md += f"- **{field['name']}**: "
                field_type = field['type']
                field_type_name = field_type['name'] or field_type['ofType']['name']
                md += f"{field_type_name} ({field_type['kind']})"
                if field['description']:
                    md += f" - {field['description']}"
                md += '\n'

            md += '\n'

    return md


def save_markdown(md):
    with open(OUTPUT_FILE, 'w') as f:
        f.write(md)


if __name__ == '__main__':
    schema = fetch_graphql_schema()
    markdown = generate_markdown(schema)
    save_markdown(markdown)
    print(f"Documentation generated and saved to {OUTPUT_FILE}")
