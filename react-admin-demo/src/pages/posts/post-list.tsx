import {
    Datagrid,
    List,
    ReferenceField,
    TextField,
    FunctionField,
    EditButton,
    TextInput,
    ReferenceInput,
} from 'react-admin';

export const PostList = () => {
    const postFilters = [
        <TextInput source="q" label="Search" alwaysOn />,
        <ReferenceInput source="userId" label="User" reference="users" />,
    ];

    return (
        <List filters={postFilters}>
            <Datagrid>
                <ReferenceField source="userId" reference="users" />
                <TextField source="id" />
                <TextField source="title" label="Post Title" />
                <FunctionField label="Excerpt" render={(record) => `${record.body.substring(0, 50)}...`} />
                <EditButton />
            </Datagrid>
        </List>
    );
}
