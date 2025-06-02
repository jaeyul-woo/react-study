import {
    Datagrid,
    List,
    TextField,
} from "react-admin";

export const UserList = () => {
    return (
        <List>
            <Datagrid>
                <TextField source="id" />
                <TextField source="name" />
                <TextField source="email" />
                <TextField source="phone" />
            </Datagrid>
        </List>
    );
}
